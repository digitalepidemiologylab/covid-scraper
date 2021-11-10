from datetime import datetime, timedelta
import logging
from logging.handlers import RotatingFileHandler
import time
import os

import boto3
from botocore.exceptions import ClientError

from constants import LOGGER_BACKUP_COUNT

LOG_FILES = ['log_wgets.txt', 'log_selenium.txt', 'log_posts.txt', 'log_csvs.txt']

# https://docs.aws.amazon.com/ses/latest/DeveloperGuide/send-using-sdk-python.html
SENDER = "Crowdbreaks <info@crowdbreaks.org>"
RECIPIENT = "olesia.altunina@epfl.ch"
AWS_REGION = "eu-central-1"
SUBJECT = "[COVID-19 Scraper] Error or Missing logs"

body_text_lag = lambda f_name: f"Recent logs could not be found for '{f_name}'.\n"
body_text_error = lambda f_name, errors: \
    f"The following errors have been found in '{f_name}':\n" \
    '\n'.join(errors)

CHARSET = "UTF-8"

client = boto3.client('ses', region_name=AWS_REGION)

MAX_PER_PERIOD = 2  # Max emails per period
PERIOD = 3600  # Period of silence in seconds

# Create logger
logger = logging.getLogger('log_watcher')
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

printout_handler = logging.StreamHandler()
writetofile_handler = RotatingFileHandler(
    'logs/log_watcher.txt', mode='a', maxBytes=5*1024*1024, 
    backupCount=LOGGER_BACKUP_COUNT, encoding=None, delay=0)

printout_handler.setLevel(logging.INFO)
printout_handler.setFormatter(formatter)
writetofile_handler.setLevel(logging.INFO)
writetofile_handler.setFormatter(formatter)

logger.addHandler(printout_handler)
logger.addHandler(writetofile_handler)


def send_email(messages):
    return client.send_email(
        Destination={
            'ToAddresses': [
                RECIPIENT,
            ],
        },
        Message={
            'Body': {
                'Text': {
                    'Charset': CHARSET,
                    'Data': '\n'.join(messages),
                },
                'Html': {
                    'Charset': CHARSET,
                    'Data': '\n'.join(messages),
                }
            },
            'Subject': {
                'Charset': CHARSET,
                'Data': SUBJECT,
            },
        },
        Source=SENDER,
    )


if __name__ == '__main__':
    sent_emails = []
    not_saved = []
    start_not_saved = datetime.now()
    while True:
        if len(not_saved) > 0 and \
                (datetime.now() - start_not_saved).seconds > PERIOD:
            try:
                response = send_email(messages)
            except ClientError as e:
                logger.error(e.response['Error']['Message'])
            else:
                logger.info('Aggregated email sent! Message ID: %s.', response['MessageId'])
                start_not_saved = datetime.now()
        if len(sent_emails) > 0 and \
                (datetime.now() - max(sent_emails)).seconds > PERIOD:
            sent_emails = []
        messages = []
        for f_name in LOG_FILES:
            f_name = 'logs/' + f_name
            lines = os.popen(f'tail -n 5 {f_name}').read().split('\n')
            t = datetime.now()
            t_1 = t - timedelta(minutes=1)
            datetime_in_log = False
            has_errors = False
            errors = []
            for line in lines:
                if t.strftime('%Y-%m-%d %H:%M') in line or t_1.strftime('%Y-%m-%d %H:%M') in line:
                    datetime_in_log = True
                if 'ERROR' in line:
                    if not 'has not been saved' in line:
                        has_errors = True
                        errors.append(line)
                    else:
                        not_saved.append(line)
            message = ''
            if not datetime_in_log:
                message += body_text_lag(f_name)
            if has_errors:
                message += body_text_error(f_name, errors)
            if len(message) > 0:
                messages.append(message)
        if len(messages) > 0:
            if len(sent_emails) < MAX_PER_PERIOD:
                try:
                    response = send_email(messages)
                except ClientError as e:
                    logger.error(e.response['Error']['Message'])
                else:
                    logger.info('Email sent! Message ID: %s.', response['MessageId'])
                    sent_emails.append(datetime.now())
            else:
                logger.warning('Will not send the email (too many per hour).')
        else:
            logger.info('Everything is fine.')
        t = datetime.utcnow()
        sleeptime = 60 - (t.second + t.microsecond/1000000.0)
        time.sleep(sleeptime)
