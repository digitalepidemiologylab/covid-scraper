from datetime import datetime
from hashlib import sha512, md5
import json
import os
from pathlib import Path
import re
import time
import traceback
import shutil

from bs4 import BeautifulSoup
import pandas as pd
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, WebDriverException
from selenium.webdriver.support.expected_conditions import _find_element

from constants import POSTS, DELAY, NUM_RETRIES, GENERATED_NUMBERS_PATH


# def retry_on_error()


def only_digits(string):
    return re.sub('[^0-9]', '', string)


class Filename:
    def __init__(self, p):
        f_name, *_ = p.name.split('.')
        self.name, date, time = f_name.split('_')[-3:]
        self.datetime = datetime(*[*[int(x) for x in date.split('-')], *[int(x) for x in time.split('-')]])

    def later_than(self, other_datetime):
        return self.datetime >= other_datetime

    def earlier_than(self, other_datetime):
        return self.datetime <= other_datetime

    def in_between(self, other_datetime_min, other_datetime_max):
        return self.later_than(other_datetime_min) and self.earlier_than(other_datetime_max)


def compare_strings(soup_1, soup_2):
    hash_1, hash_2 = [sha512(soup.encode()).digest() for soup in [soup_1, soup_2]]
    return hash_1 == hash_2


def get_csv(p, sep, logger):
    if p.name.endswith('.json'):
        # with p.open('r') as f:
            # print(json.load(f))
            # print(f.read())
        return pd.read_json(str(p), orient='records')
    elif p.name.endswith('.csv'):
        try:
            return pd.read_csv(str(p), sep, index_col=False)
        except pd.errors.ParserError as exc:
            logger.error(
                '%s: %s. Traceback: %s', type(exc).__name__, str(exc),
                '; '.join(traceback.format_tb(exc.__traceback__)))
    else:
        logger.error(f"The format of file '{p.name}' should be CSV or JSON.")


def get_soup(p):
    with p.open('rb') as f:
        return BeautifulSoup(f.read(), 'html.parser')


def rename_path_with_suffix(path, suffix):
    ppath, extension = path.split('.')
    new_path = ppath + suffix + '.' + extension
    os.rename(path, new_path)


def remove_if_needed(
    p_2, country, t, arg_1, arg_2, num_1, num_2, logger
):
    remove = False
    if country in POSTS:
        if compare_strings(arg_1, arg_2):
            remove = True
    else:
        if num_1 and num_2:
            if num_1 == num_2:
                remove = True
        elif compare_strings(arg_1, arg_2):
            remove = True
    if remove:
        try:
            os.remove(p_2)
        except FileNotFoundError:
            logger.error("File '%s' not found.", p_2)
        except PermissionError:
            logger.error("You have no permission to remove the file '%s'.", p_2)
    else:
        logger.info("The file '%s' has changed. Keeping the new version.", p_2)
        numbers = {}
        with open('logs/numbers.json', 'rb') as f:
            numbers = json.load(f)
        with open('logs/numbers.json', 'w') as f:
            if not numbers.get(country):
                numbers[country] = {t: num_2}
            else:
                numbers[country][t] = num_2
            json.dump(numbers, f)


def remove_latest_if_csv_unchanged(p_1, p_2, country, sep, t, Csv, logger):
    csv_1, csv_2 = [get_csv(p, sep, logger) for p in [p_1, p_2]]
    num_1 = None
    num_2 = None
    try:
        csv_1, num_1 = getattr(Csv, country.lower())(csv_1)
        csv_2, num_2 = getattr(Csv, country.lower())(csv_2)
    except AssertionError:
        logger.warning("The structure of the file '%s' have changed. Check the source.", p_2)
        os.rename(str(p_2), os.path.join(p_2.parents[0], 'processing_exception', p_2.name))
    except Exception as exc:
        logger.error('%s: %s. Traceback: %s', type(exc).__name__, str(exc), '; '.join(traceback.format_tb(exc.__traceback__)))
        os.rename(p_2, os.path.join(p_2.parents[0], 'processing_exception', p_2.name))
    else:
        logger.debug('%s: %s %s', country, num_1, num_2)
        remove_if_needed(
            p_2, country, t, csv_1, csv_2, num_1, num_2, logger
        )


def remove_latest_if_page_unchanged(p_1, p_2, country, t, Soup, logger):
    try:
        soup_1, soup_2 = [get_soup(p) for p in [p_1, p_2]]
    except UnicodeDecodeError:
        logger.warning('Unicode decode error.')
        return
    num_1 = None
    num_2 = None
    try:
        soup_1, num_1 = getattr(Soup, country.lower())(soup_1)
        soup_2, num_2 = getattr(Soup, country.lower())(soup_2)
    except AssertionError:
        logger.warning("The structure of the file '%s' has changed. Check the source.", p_2)
        os.rename(p_2, os.path.join(p_2.parents[0], 'processing_exception', p_2.name))
    except Exception as exc:
        logger.error('%s: %s. Traceback: %s', type(exc).__name__, str(exc), '; '.join(traceback.format_tb(exc.__traceback__)))
        os.rename(p_2, os.path.join(p_2.parents[0], 'processing_exception', p_2.name))
    else:
        logger.debug('%s: %s %s', country, num_1, num_2)
        remove_if_needed(
            p_2, country, t, soup_1, soup_2, num_1, num_2, logger
        )


# Fixing a mess
def copy_if_changed(
    p_2, country, arg_1, arg_2, num_1, num_2, logger
):
    copy = True
    if country in POSTS:
        if compare_strings(arg_1, arg_2):
            copy = False
    else:
        if num_1 and num_2:
            if num_1 == num_2:
                copy = False
        elif compare_strings(arg_1, arg_2):
            copy = False
    if copy:
        name = Path(p_2).name
        name = name if name.split('.')[-1] == 'html' else '.'.join(name.split('.')[:-1])
        logger.info(f'NAME: data/{name}')
        shutil.copyfile(p_2, f'data/{name}')
        logger.info("The file '%s' has changed. Keeping the new version.", p_2)
        numbers = {}
        with open('logs/numbers.json', 'rb') as f:
            numbers = json.load(f)
        with open('logs/numbers.json', 'w') as f:
            t = Filename(p_2).datetime.strftime('%Y-%m-%d_%H-%M-%S')
            if not numbers.get(country):
                numbers[country] = {t: num_2}
            else:
                numbers[country][t] = num_2
            json.dump(numbers, f)


def copy_latest_if_csv_changed(p_1, p_2, country, sep, Csv, logger):
    logger.info(p_2)
    csv_1, csv_2 = [get_csv(p, sep, logger) for p in [p_1, p_2]]
    num_1 = None
    num_2 = None
    try:
        csv_1, num_1 = getattr(Csv, country.lower())(csv_1)
        csv_2, num_2 = getattr(Csv, country.lower())(csv_2)
    except AssertionError:
        logger.warning("The structure of the file '%s' has changed. Check the source.", p_2)
    except Exception as exc:
        logger.error('%s: %s. Traceback: %s', type(exc).__name__, str(exc), '; '.join(traceback.format_tb(exc.__traceback__)))
    else:
        logger.debug('%s: %s %s', country, num_1, num_2)
        copy_if_changed(
            p_2, country, csv_1, csv_2, num_1, num_2, logger
        )


def copy_latest_if_page_changed(p_1, p_2, country, Soup, logger):
    logger.info(p_2)
    try:
        soup_1, soup_2 = [get_soup(p) for p in [p_1, p_2]]
    except UnicodeDecodeError:
        logger.warning('Unicode decode error.')
        return
    num_1 = None
    num_2 = None
    try:
        soup_1, num_1 = getattr(Soup, country.lower())(soup_1)
        soup_2, num_2 = getattr(Soup, country.lower())(soup_2)
    except AssertionError:
        logger.warning("The structure of the file '%s' has changed. Check the source.", p_2)
    except Exception as exc:
        logger.error('%s: %s. Traceback: %s', type(exc).__name__, str(exc), '; '.join(traceback.format_tb(exc.__traceback__)))
    else:
        logger.debug('%s: %s %s', country, num_1, num_2)
        copy_if_changed(
            p_2, country, soup_1, soup_2, num_1, num_2, logger
        )


# Send to numbers
def send_to_numbers(p, country, num):
    numbers = {}
    with open(GENERATED_NUMBERS_PATH, 'rb') as f:
        numbers = json.load(f)
    with open(GENERATED_NUMBERS_PATH, 'w') as f:
        t = Filename(p).datetime.strftime('%Y-%m-%d_%H-%M-%S')
        if not numbers.get(country):
            numbers[country] = {t: num}
        else:
            numbers[country][t] = num
        json.dump(numbers, f)


def send_to_numbers_csv(p, country, sep, Csv, logger):
    csv = get_csv(p, sep, logger)
    num = None
    try:
        csv, num = getattr(Csv, country.lower())(csv)
    except AssertionError:
        logger.warning("The structure of the file '%s' has changed. Check the source.", p)
    except Exception as exc:
        logger.error("'%s' %s: %s", p, type(exc).__name__, str(exc))
    else:
        logger.debug('%s: %s %s', country, num)
        send_to_numbers(p, country, num)


def send_to_numbers_html(p, country, Soup, logger):
    try:
        soup = get_soup(p)
    except UnicodeDecodeError:
        logger.warning('Unicode decode error.')
        return
    num = None
    try:
        soup, num = getattr(Soup, country.lower())(soup)
    except AssertionError:
        logger.warning("The structure of the file '%s' has changed. Check the source.", p)
    except Exception as exc:
        logger.error("'%s' %s: %s", p, type(exc).__name__, str(exc))
    else:
        logger.debug('%s: %s %s', country, num)
        if num is None:
            if soup is not None:
                send_to_numbers(p, country, md5(soup.encode()).hexdigest())
            else:
                pass
        else:
            send_to_numbers(p, country, num)


# class text_match(object):
#     def __init__(self, locator, regexp):
#         self.locator = locator
#         self.regexp = regexp

#     def __call__(self, driver):
#         element_text = _find_element(driver, self.locator).text
#         if self.regexp is None:
#             return element_text
#         else:
#             return re.search(re.compile(self.regexp), element_text)


def wait_until_xpath(
    browser, url, xpath, logger, *, before_wait=None, errors=0, sleep=1
):
    try:
        browser.get(url)
        if before_wait is not None:
            before_wait(browser)
        # WebDriverWait(browser, DELAY).until(text_match((By.XPATH, xpath), pattern))
        WebDriverWait(browser, DELAY).until(
            EC.presence_of_element_located((
                By.XPATH,
                xpath
            ))
        )
        time.sleep(sleep)
        return False
    except TimeoutException:
        errors += 1
        logger.warning("Request for '%s' timed out. Retrying.", url)
        if errors < NUM_RETRIES:
            wait_until_xpath(
                browser, url, xpath, logger,
                before_wait=before_wait, errors=errors, sleep=sleep)
        else:
            logger.error("Info for '%s' could not be loaded.", url)
            return True
    except Exception as exc:
        logger.error("'%s' %s: %s", url, type(exc).__name__, str(exc))
