import argparse
from datetime import datetime
import logging
from logging.handlers import RotatingFileHandler
import os
from pathlib import Path
import time

from constants import WEBSITES, WGET_DOWNLOADS, SELENIUM_DOWNLOADS, POSTS, CSVS, LOGGER_BACKUP_COUNT, GENERATED_NUMBERS_PATH
from helpers import send_to_numbers_csv, send_to_numbers_html
from pandas_csvs import Csv
from soup_posts import SoupPosts
from soup_wgets import SoupWgets
from soup_selenium import SoupSelenium

from selenium import webdriver
from selenium.webdriver.firefox.options import Options

from helpers import Filename

# Create logger
logger = logging.getLogger('generate_numbers')
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

printout_handler = logging.StreamHandler()
writetofile_handler = RotatingFileHandler(
    'logs/log_generate_numbers.txt', mode='a', maxBytes=5*1024*1024, 
    backupCount=LOGGER_BACKUP_COUNT, encoding=None, delay=0)

printout_handler.setLevel(logging.INFO)
printout_handler.setFormatter(formatter)
writetofile_handler.setLevel(logging.INFO)
writetofile_handler.setFormatter(formatter)

logger.addHandler(printout_handler)
logger.addHandler(writetofile_handler)


# Create browser
global browser
options = Options()
options.headless = True
browser = webdriver.Firefox(options=options)
SoupPosts.set_browser(browser)


# Argparser
parser = argparse.ArgumentParser(description='Generate numbers.json')
parser.add_argument('--later', type=str, default=None,
                    help="generate later than the date, format: '%Y-%m-%d_%H-%M-%S'")


def get_paths(country, later=None):
    ps = sorted([
        p for p in Path('data').iterdir()
        if p.name.startswith(f'{country.lower()}_') and
        p.name.split('.')[-1] == 'html'
    ])
    if later is not None:
        for p in ps:
            if Filename(p).later_than(later):
                return ps[ps.index(p):]
    return ps


if __name__ == '__main__':
    args = parser.parse_args()
    if args.later is None:
        later = args.later
    else:
        later = datetime.strptime(args.later, '%Y-%m-%d_%H-%M-%S')

    numbers_path = Path(GENERATED_NUMBERS_PATH)
    with numbers_path.open('w') as f:
        f.write('{}')

    wget_websites = [k for k in WEBSITES if k in WGET_DOWNLOADS]
    for country in wget_websites:
        ps = get_paths(country, later)
        for p in ps:
            try:
                send_to_numbers_html(p, country, SoupWgets, logger)
            except FileNotFoundError:
                pass

    selenium_websites = [k for k in WEBSITES if k in SELENIUM_DOWNLOADS]
    for country in selenium_websites:
        ps = get_paths(country, later)
        for p in ps:
            try:
                send_to_numbers_html(p, country, SoupSelenium, logger)
            except FileNotFoundError:
                pass

    posts_websites = [k for k in WEBSITES if k in POSTS]
    for country in posts_websites:
        ps = get_paths(country, later)
        for p in ps:
            try:
                send_to_numbers_html(p, country, SoupPosts, logger)
            except FileNotFoundError:
                pass

    csvs_websites = [k for k in WEBSITES if k in CSVS]
    for country in csvs_websites:
        ps = get_paths(country, later)
        for p in ps:
            try:
                send_to_numbers_csv(p, country, CSVS[country], Csv, logger)
            except FileNotFoundError:
                pass
