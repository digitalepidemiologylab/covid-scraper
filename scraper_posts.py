from datetime import datetime
import logging
from logging.handlers import RotatingFileHandler
import os
from pathlib import Path
import sys
import time

from selenium import webdriver
from selenium.webdriver.firefox.options import Options

from constants import WEBSITES, POSTS, LOGGER_BACKUP_COUNT
from helpers import remove_latest_if_page_unchanged
from soup_posts import SoupPosts

# Create logger
logger = logging.getLogger('scraper_posts')
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

printout_handler = logging.StreamHandler()
writetofile_handler = RotatingFileHandler(
    'logs/log_posts.txt', mode='a', maxBytes=5*1024*1024, 
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


if __name__ == '__main__':
    try:
        while True:
            user = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) ' \
                'AppleWebKit/605.1.15 (KHTML, like Gecko) ' \
                'Version/13.1 Safari/605.1.15'
            start_time = time.time()
            posts_websites = {
                k: v for k, v in WEBSITES.items() if k in POSTS}
            for country, url in posts_websites.items():
                t = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
                p = f"data/{country.lower()}_{t}.html"
                command = f'wget -4 -O "{p}" -U "{user}" --connect-timeout=1 --read-timeout=10 --limit-rate=500K -e robots=off "{url}"'
                os.system(command)
                try:
                    if os.stat(p).st_size == 0:
                        os.remove(p)
                except FileNotFoundError as exc:
                    logger.warning('%s: %s', type(exc).__name__, str(exc))
                    continue
                ps = sorted([os.path.join('data', p.name) for p in Path('data').iterdir() if p.name.startswith(country.lower())])
                if len(ps) in [0, 1]:
                    continue
                if ps[-1] != p:
                    logger.error("File '%s' has not been saved.", p)
                    continue
                remove_latest_if_page_unchanged(*ps[-2:], country, t, SoupPosts, logger)
            full_cycle = time.time() - start_time
            logger.info('CYCLE COMPLETE: %d s', time.time() - start_time)
            # break
            t = datetime.utcnow()
            sleeptime = 60 - (t.second + t.microsecond/1000000.0)
            time.sleep(sleeptime)
            # if int(full_cycle) < 60:
            #     sleep(60 - int(full_cycle))
    except KeyboardInterrupt:
        browser.close()
        sys.exit()
