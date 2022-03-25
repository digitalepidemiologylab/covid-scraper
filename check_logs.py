from datetime import datetime, timedelta
from dateutil import parser
import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

from constants import LOGGER_BACKUP_COUNT, LOG_FILES

# Create logger
logger = logging.getLogger('check_logs')
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

printout_handler = logging.StreamHandler()
writetofile_handler = RotatingFileHandler(
    'logs/log_check_logs.txt', mode='a', maxBytes=5*1024*1024, 
    backupCount=LOGGER_BACKUP_COUNT, encoding=None, delay=0)

printout_handler.setLevel(logging.INFO)
printout_handler.setFormatter(formatter)
writetofile_handler.setLevel(logging.INFO)
writetofile_handler.setFormatter(formatter)

logger.addHandler(printout_handler)
logger.addHandler(writetofile_handler)


if __name__ == '__main__':
    for f_name in LOG_FILES:
        logger.info(f_name)
        ps = sorted([p for p in Path('logs').iterdir() if p.name.startswith(f_name)])
        for p in ps:
            logger.info(str(p))
            with p.open('r') as f:
                logs = f.readlines()
                logs = [(i + 1, line) for i, line in enumerate(logs)]
                logs = [line for line in logs if line[1].startswith('2022')]
                for i in range(len(logs) - 1):
                    datetime_current = parser.parse(logs[i][1][:23])
                    datetime_next = parser.parse(logs[i + 1][1][:23])
                    time_gap = datetime_next - datetime_current

                    if time_gap > timedelta(minutes=10):
                        logger.info(
                            f"{datetime_current.strftime('%Y-%m-%d')}, "
                            f'line {logs[i][0]}: {time_gap}.')
