from hashlib import sha512
import json
import os
import re
import time
import traceback

from bs4 import BeautifulSoup
import pandas as pd
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.expected_conditions import _find_element

from constants import POSTS, DELAY, NUM_RETRIES


def compare_strings(soup_1, soup_2):
    hash_1, hash_2 = [sha512(soup.encode()).digest() for soup in [soup_1, soup_2]]
    return hash_1 == hash_2


def get_csv(p, sep):
    return pd.read_csv(p, sep)


def get_soup(p):
    with open(p, 'rb') as f:
        return BeautifulSoup(f.read(), 'html.parser')


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
            logger.error('File "%s" not found.', p_2)
        except PermissionError:
            logger.error('You have no permission to remove the file "%s".', p_2)
    else:
        logger.info('The file "%s" has changed. Keeping the new version.', p_2)
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
    csv_1, csv_2 = [get_csv(p, sep) for p in [p_1, p_2]]
    num_1 = None
    num_2 = None
    try:
        csv_1, num_1 = getattr(Csv, country.lower())(csv_1)
        csv_2, num_2 = getattr(Csv, country.lower())(csv_2)
    except AssertionError:
        logger.warning('The structure of the file "%s" have changed. Check the source.', p_2)
    except Exception as exc:
        logger.error('%s: %s\nTraceback:\n%s', type(exc).__name__, str(exc), '\n'.join(traceback.format_tb(exc.__traceback__)))
    logger.debug('%s: %s %s', country, num_1, num_2)
    remove_if_needed(
        p_2, country, t, csv_1, csv_2, num_1, num_2, logger
    )
    return


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
        logger.warning('The structure of the file "%s" have changed. Check the source.', p_2)
    except Exception as exc:
        logger.error('%s: %s\nTraceback:\n%s', type(exc).__name__, str(exc), '\n'.join(traceback.format_tb(exc.__traceback__)))
    logger.debug('%s: %s %s', country, num_1, num_2)
    remove_if_needed(
        p_2, country, t, soup_1, soup_2, num_1, num_2, logger
    )
    return


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


def wait_until_xpath(browser, url, xpath, logger, errors=0):
    try:
        browser.get(url)
        # WebDriverWait(browser, DELAY).until(text_match((By.XPATH, xpath), pattern))
        WebDriverWait(browser, DELAY).until(
            EC.presence_of_element_located((
                By.XPATH,
                xpath
            ))
        )
        time.sleep(1)
        return False
    except TimeoutException:
        errors += 1
        logger.error("Request for '%s' timed out. Retrying.", url)
        if errors < NUM_RETRIES:
            wait_until_xpath(browser, url, xpath, logger, errors)
        else:
            logger.error("Info for '%s' could not be loaded.", url)
            return True
