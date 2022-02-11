from datetime import datetime
import logging
from logging.handlers import RotatingFileHandler
import os
from pathlib import Path
import time

from constants import WEBSITES, WGET_DOWNLOADS, SELENIUM_DOWNLOADS, POSTS, CSVS, LOGGER_BACKUP_COUNT
from helpers import (remove_latest_if_page_unchanged,
                     remove_latest_if_csv_unchanged,
                     copy_latest_if_page_changed,
                     copy_latest_if_csv_changed,
                     Filename)
from pandas_csvs import Csv
from soup_posts import SoupPosts
from soup_wgets import SoupWgets
from soup_selenium import SoupSelenium

from selenium import webdriver
from selenium.webdriver.firefox.options import Options

# Create logger
logger = logging.getLogger('scraper_fix')
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

printout_handler = logging.StreamHandler()
writetofile_handler = RotatingFileHandler(
    'logs/log_fix.txt', mode='a', maxBytes=5*1024*1024, 
    backupCount=LOGGER_BACKUP_COUNT, encoding=None, delay=0)

printout_handler.setLevel(logging.INFO)
printout_handler.setFormatter(formatter)
writetofile_handler.setLevel(logging.INFO)
writetofile_handler.setFormatter(formatter)

logger.addHandler(printout_handler)
logger.addHandler(writetofile_handler)


# Create browser
# global browser
# options = Options()
# options.headless = True
# browser = webdriver.Firefox(options=options)
# SoupPosts.set_browser(browser)


if __name__ == '__main__':
    country = 'Poland'
    ps = sorted([p for p in Path('data/processing_exception').iterdir() if p.name.startswith(f'{country.lower()}_2022-02') and p.name.endswith('html')])
    for i in range(len(ps) - 1):
        t = Filename(ps[i + 1]).datetime.strftime('%Y-%m-%d_%H-%M-%S')
        copy_latest_if_page_changed(ps[i], ps[i + 1], country, SoupSelenium, logger)

    # country = 'Monaco'
    # ps = sorted([p for p in Path('data/processing_exception').iterdir() if p.name.startswith(f'{country.lower()}_2022-02') and p.name.endswith('html')])
    # for i in range(len(ps) - 1):
    #     t = Filename(ps[i + 1]).datetime.strftime('%Y-%m-%d_%H-%M-%S')
    #     copy_latest_if_page_changed(ps[i], ps[i + 1], country, SoupPosts, logger)

    # country = 'Lithuania'
    # ps = sorted([p for p in Path('data/processing_exception').iterdir() if p.name.startswith(f'{country.lower()}_2022-02') and p.name.endswith('html')])
    # for i in range(len(ps) - 1):
    #     t = Filename(ps[i + 1]).datetime.strftime('%Y-%m-%d_%H-%M-%S')
    #     copy_latest_if_page_changed(ps[i], ps[i + 1], country, SoupSelenium, logger)

    # country = 'Germany'
    # ps = sorted([p for p in Path('data/processing_exception').iterdir() if p.name.startswith(f'{country.lower()}_2022-01') and p.name.endswith('html')])
    # for i in range(len(ps) - 1):
    #     t = Filename(ps[i + 1]).datetime.strftime('%Y-%m-%d_%H-%M-%S')
    #     copy_latest_if_page_changed(ps[i], ps[i + 1], country, SoupWgets, logger)

    # country = 'Lithuania'
    # ps = sorted([p for p in Path('data/processing_exception').iterdir() if p.name.startswith(f'{country.lower()}_2022-01') and p.name.endswith('html')])
    # for i in range(len(ps) - 1):
    #     t = Filename(ps[i + 1]).datetime.strftime('%Y-%m-%d_%H-%M-%S')
    #     copy_latest_if_page_changed(ps[i], ps[i + 1], country, SoupSelenium, logger)

    # country = 'San_Marino'
    # ps = sorted([
    #     p for p in Path('data/processing_exception').iterdir()
    #     if p.name.startswith(country.lower()) and p.name.endswith('html') and
    #     Filename(p).later_than(datetime(2021, 12, 26)) and
    #     Filename(p).earlier_than(datetime(2022, 1, 4))
    # ])
    # print(len(ps))
    # for i in range(len(ps) - 1):
    #     t = Filename(ps[i + 1]).datetime.strftime('%Y-%m-%d_%H-%M-%S')
    #     copy_latest_if_page_changed(ps[i], ps[i + 1], country, SoupPosts, logger)

    # country = 'Gibraltar'
    # ps = sorted([p for p in Path('data/processing_exception').iterdir() if p.name.startswith(f'{country.lower()}_2022-01') and p.name.endswith('html')])
    # for i in range(len(ps) - 1):
    #     t = Filename(ps[i + 1]).datetime.strftime('%Y-%m-%d_%H-%M-%S')
    #     copy_latest_if_page_changed(ps[i], ps[i + 1], country, SoupWgets, logger)

    # country = 'Azerbaijan'
    # ps = sorted([p for p in Path('data/processing_exception').iterdir() if p.name.startswith(f'{country.lower()}_2022-01') and p.name.endswith('html')])
    # for i in range(len(ps) - 1):
    #     t = Filename(ps[i + 1]).datetime.strftime('%Y-%m-%d_%H-%M-%S')
    #     copy_latest_if_page_changed(ps[i], ps[i + 1], country, SoupWgets, logger)

    # country = 'Russia'
    # ps = sorted([p for p in Path('data/processing_exception').iterdir() if p.name.startswith(f'{country.lower()}_2022-01') and p.name.endswith('html')])
    # for i in range(len(ps) - 1):
    #     t = Filename(ps[i + 1]).datetime.strftime('%Y-%m-%d_%H-%M-%S')
    #     copy_latest_if_page_changed(ps[i], ps[i + 1], country, SoupWgets, logger)

    # country = 'Gibraltar'
    # ps = sorted([p for p in Path('data/processing_exception').iterdir() if p.name.startswith(country.lower()) and p.name.endswith('html')])
    # for i in range(len(ps) - 1):
    #     t = Filename(ps[i + 1]).datetime.strftime('%Y-%m-%d_%H-%M-%S')
    #     copy_latest_if_page_changed(ps[i], ps[i + 1], country, SoupWgets, logger)

    # country = 'Israel'
    # ps = sorted([p for p in Path('data').iterdir() if p.name.startswith(country.lower())])
    # for i in range(len(ps) - 1):
    #     try:
    #         t = Filename(ps[i + 1]).datetime.strftime('%Y-%m-%d_%H-%M-%S')
    #         remove_latest_if_page_unchanged(ps[i], ps[i + 1], country, t, SoupSelenium, logger)
    #     except FileNotFoundError:
    #         logger.info('File not found.')

    # wget_websites = [k for k in WEBSITES if k in WGET_DOWNLOADS]
    # for country in wget_websites:
    #     ps = sorted([p for p in Path('data').iterdir() if p.name.startswith(country.lower())])
    #     for i in range(len(ps) - 1):
    #         remove_latest_if_page_unchanged(ps[i], ps[i + 1], country, SoupWgets, logger)


    # Fixing processing exception of Gibraltar
    # country = 'Gibraltar'
    # ps = sorted([str(p) for p in Path(f'data').iterdir() if p.name.split('.')[-1] == 'processing_exception'])
    # for i in range(len(ps) - 1):
    #     copy_latest_if_page_changed(ps[i], ps[i + 1], country, SoupWgets, logger)

    # Fixing not filtered files (everything was saved)
    # wget_websites = [k for k in WEBSITES if k in WGET_DOWNLOADS]
    # for country in wget_websites:
    #     ps = sorted([str(p) for p in Path(f'data/{country.lower()}').iterdir()])
    #     for i in range(len(ps) - 1):
    #         copy_latest_if_page_changed(ps[i], ps[i + 1], country, SoupWgets, logger)

    # selenium_websites = [k for k in WEBSITES if k in SELENIUM_DOWNLOADS]
    # for country in selenium_websites:
    #     ps = sorted([str(p) for p in Path(f'data/{country.lower()}').iterdir()])
    #     for i in range(len(ps) - 1):
    #         copy_latest_if_page_changed(ps[i], ps[i + 1], country, SoupSelenium, logger)

    # posts_websites = [k for k in WEBSITES if k in POSTS]
    # for country in posts_websites:
    #     ps = sorted([str(p) for p in Path(f'data/{country.lower()}').iterdir()])
    # country = 'San_Marino'
    # datetime_min = datetime(2021, 11, 9, 19, 55)
    # datetime_max = datetime(2021, 11, 14, 11, 30)
    # ps = sorted([str(p) for p in Path(f'data/{country.lower()}').iterdir() if Filename(p).later_than(datetime_min)])
    # for i in range(len(ps) - 1):
    #     copy_latest_if_page_changed(ps[i], ps[i + 1], country, SoupPosts, logger)

    # csvs_websites = [k for k in WEBSITES if k in CSVS]
    # for country in csvs_websites:
    # country = 'Netherlands'
    # datetime_min = datetime(2021, 11, 11, 3)
    # datetime_max = datetime(2021, 11, 14, 11, 30)
    # ps = sorted([str(p) for p in Path(f'data/{country.lower()}').iterdir() if Filename(p).later_than(datetime_min)])
    # for i in range(len(ps) - 1):
    #     copy_latest_if_csv_changed(ps[i], ps[i + 1], country, CSVS[country], Csv, logger)
