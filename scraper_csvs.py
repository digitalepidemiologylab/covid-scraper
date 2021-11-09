from datetime import datetime
import logging
from logging.handlers import RotatingFileHandler
import os
from pathlib import Path
import time

from constants import WEBSITES, CSVS
from helpers import remove_latest_if_csv_unchanged
from pandas_csvs import Csv

# Create logger
logger = logging.getLogger('scraper_csvs')
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

printout_handler = logging.StreamHandler()
writetofile_handler = RotatingFileHandler(
    'logs/log_csvs.txt', mode='a', maxBytes=5*1024*1024, 
    backupCount=2, encoding=None, delay=0)

printout_handler.setLevel(logging.INFO)
printout_handler.setFormatter(formatter)
writetofile_handler.setLevel(logging.INFO)
writetofile_handler.setFormatter(formatter)

logger.addHandler(printout_handler)
logger.addHandler(writetofile_handler)


if __name__ == '__main__':
    while True:
        user = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) ' \
            'AppleWebKit/605.1.15 (KHTML, like Gecko) ' \
            'Version/13.1 Safari/605.1.15'
        start_time = time.time()
        wget_websites = {
            k: v for k, v in WEBSITES.items() if k in CSVS.keys()}
        for country, url in wget_websites.items():
            t = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
            p = f"data/{country.lower()}_{t}.csv"
            command = f'wget -4 -O "{p}" -U "{user}" --connect-timeout=1 --read-timeout=10 -e robots=off "{url}"'
            os.system(command)
            if os.stat(p).st_size == 0:
                os.remove(p)
            ps = sorted([p.name for p in Path('.').iterdir() if p.name.startswith(country.lower())])
            if len(ps) in [0, 1]:
                continue
            if ps[-1] != p:
                logger.error('File "%s" has not been saved.', p)
                continue
            remove_latest_if_csv_unchanged(*ps[-2:], country, CSVS[country], t, Csv, logger)
        full_cycle = time.time() - start_time
        logger.info('CYCLE COMPLETE: %d s', time.time() - start_time)
        # break
        t = datetime.utcnow()
        sleeptime = 60 - (t.second + t.microsecond/1000000.0)
        time.sleep(sleeptime)
        # if int(full_cycle) < 60:
        #     sleep(60 - int(full_cycle))
