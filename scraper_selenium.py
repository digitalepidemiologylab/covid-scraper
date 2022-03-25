from datetime import datetime
import logging
from logging.handlers import RotatingFileHandler
import os
from pathlib import Path
import sys
import time

from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.common.exceptions import WebDriverException

from constants import SLEEPS, WEBSITES, SELENIUM_DOWNLOADS, XPATHS, LOGGER_BACKUP_COUNT, BEFORE_WAIT
from helpers import remove_latest_if_page_unchanged, wait_until_xpath
from soup_selenium import SoupSelenium

# Create logger
logger = logging.getLogger('scraper_selenium')
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

printout_handler = logging.StreamHandler()
writetofile_handler = RotatingFileHandler(
    'logs/log_selenium.txt', mode='a', maxBytes=5*1024*1024, 
    backupCount=LOGGER_BACKUP_COUNT, encoding=None, delay=0)

printout_handler.setLevel(logging.INFO)
printout_handler.setFormatter(formatter)
writetofile_handler.setLevel(logging.INFO)
writetofile_handler.setFormatter(formatter)

logger.addHandler(printout_handler)
logger.addHandler(writetofile_handler)


if __name__ == '__main__':
    # Create browser
    global browser
    options = Options()
    options.headless = True
    browser = webdriver.Firefox(options=options)
    overtime_count = 0
    try:
        while True:
            user = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) ' \
                'AppleWebKit/605.1.15 (KHTML, like Gecko) ' \
                'Version/13.1 Safari/605.1.15'
            start_time = time.time()
            selenium_websites = {
                k: v for k, v in WEBSITES.items() if k in SELENIUM_DOWNLOADS}
            for country, url in selenium_websites.items():
                t = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
                p = f"data/{country.lower()}_{t}.html"
                errors = 0
                continuee = wait_until_xpath(
                    browser, url, XPATHS[country], logger,
                    before_wait=BEFORE_WAIT.get(country, None), errors=errors,
                    sleep=SLEEPS.get(country, 1))
                if continuee is True:
                    continue
                try:
                    source = browser.page_source
                except WebDriverException:
                    continue
                with open(p, 'w') as f:
                    logger.debug('Written page source to file %s', p)
                    f.write(source)
                if os.stat(p).st_size == 0:
                    os.remove(p)
                ps = sorted([p for p in Path('data').iterdir() if p.name.startswith(country.lower())])
                if len(ps) in [0, 1]:
                    continue
                if str(ps[-1]) != str(p):
                    logger.error("File '%s' has not been saved.", p)
                    continue
                remove_latest_if_page_unchanged(*ps[-2:], country, t, SoupSelenium, logger)
            full_cycle = time.time() - start_time
            logger.info('CYCLE COMPLETE: %d s', time.time() - start_time)
            # break
            if full_cycle > 60:
                overtime_count += 1
                if overtime_count > 2:
                    overtime_count = 0
                    browser.close()
                    browser = webdriver.Firefox(options=options)
                    logger.info('Browser reloaded')
                sleeptime = 0
            else:
                t = datetime.utcnow()
                sleeptime = 60 - (t.second + t.microsecond/1000000.0)
                time.sleep(sleeptime)
            # if int(full_cycle) < 60:
            #     sleep(60 - int(full_cycle))
    except KeyboardInterrupt:
        browser.close()
        sys.exit()
