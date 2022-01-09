from datetime import datetime
import logging
from logging.handlers import RotatingFileHandler
import os
from pathlib import Path
import time

from constants import WEBSITES, WGET_DOWNLOADS, LOGGER_BACKUP_COUNT
from helpers import remove_latest_if_page_unchanged
from soup_wgets import SoupWgets

# Create logger
logger = logging.getLogger('scraper_wgets')
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

printout_handler = logging.StreamHandler()
writetofile_handler = RotatingFileHandler(
    'logs/log_wgets.txt', mode='a', maxBytes=5*1024*1024, 
    backupCount=LOGGER_BACKUP_COUNT, encoding=None, delay=0)

printout_handler.setLevel(logging.INFO)
printout_handler.setFormatter(formatter)
writetofile_handler.setLevel(logging.INFO)
writetofile_handler.setFormatter(formatter)

logger.addHandler(printout_handler)
logger.addHandler(writetofile_handler)


if __name__ == '__main__':
    # TODO: Force reload if takes more tham 30 s
    while True:
        user = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) ' \
            'AppleWebKit/605.1.15 (KHTML, like Gecko) ' \
            'Version/13.1 Safari/605.1.15'
        start_time = time.time()
        wget_websites = {
            k: v for k, v in WEBSITES.items() if k in WGET_DOWNLOADS}
        logger.info(wget_websites.keys())
        for country, url in wget_websites.items():
            t = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
            p = f"data/{country.lower()}_{t}.html"
            command = f'wget -4 -O "{p}" -U "{user}" --connect-timeout=1 --read-timeout=10 --limit-rate=500K -e robots=off "{url}"'
            os.system(command)
            try:
                if os.stat(p).st_size == 0:
                    os.remove(p)
            except FileNotFoundError as exc:
                # TODO: Do retry wget
                logger.warning('%s: %s', type(exc).__name__, str(exc))
                continue
            ps = sorted([p for p in Path('data').iterdir() if p.name.startswith(country.lower())])
            if len(ps) in [0, 1]:
                continue
            if str(ps[-1]) != str(p):
                logger.error("File '%s' has not been saved.", p)
                continue
            remove_latest_if_page_unchanged(*ps[-2:], country, t, SoupWgets, logger)
        full_cycle = time.time() - start_time
        logger.info('CYCLE COMPLETE: %d s', time.time() - start_time)
        # break
        t = datetime.utcnow()
        sleeptime = 60 - (t.second + t.microsecond/1000000.0)
        time.sleep(sleeptime)
        # if int(full_cycle) < 60:
        #     sleep(60 - int(full_cycle))
