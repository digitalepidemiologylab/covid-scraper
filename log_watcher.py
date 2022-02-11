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
SUBJECT_PREFIX = "[COVID-19 Scraper] "

body_text_lag = lambda f_name: f"Recent logs could not be found for '{f_name}'.\n"

CHARSET = "UTF-8"

client = boto3.client('ses', region_name=AWS_REGION)

MAX_PER_PERIOD = 2  # Max emails per period
PERIOD = 3600  # Period of silence in seconds
AGGREGATED_PERIOD = 3600 * 6
WARNING_PERIOD = 3600 * 6
OLD_BUFFER = 20  # How many old messages to keep for comparison

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


def send_email(messages, subject):
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
                    'Data': '<br>'.join(messages),
                }
            },
            'Subject': {
                'Charset': CHARSET,
                'Data': SUBJECT_PREFIX + subject,
            },
        },
        Source=SENDER,
    )

aggregated_phrases = [
    'has not been saved',
    'timed out. Retrying.'
]
aggregated_conditions = lambda line: any([phrase in line for phrase in aggregated_phrases])


if __name__ == '__main__':
    logger.info('Started script')
    sent_emails = []
    aggregated = []
    warnings = []
    missing_logs_old = []
    unexpected_errors_old = []
    start_aggregated = datetime.now()
    start_warnings = datetime.now()
    while True:
        if len(aggregated) > 5 and \
                (datetime.now() - start_aggregated).seconds > AGGREGATED_PERIOD:
            try:
                aggregated = [log if 'israel' not in log else 'Israel' for log in aggregated]
                response = send_email(list(dict.fromkeys(aggregated)), 'Aggregated Errors')
            except ClientError as e:
                logger.error(e.response['Error']['Message'])
            else:
                logger.info('Aggregated email sent! Message ID: %s.', response['MessageId'])
                start_aggregated = datetime.now()
                aggregated = []
        if len(warnings) > 10 and \
                (datetime.now() - start_warnings).seconds > AGGREGATED_PERIOD:
            try:
                response = send_email(list(dict.fromkeys(warnings)), 'Aggregated Warnings')
            except ClientError as e:
                logger.error(e.response['Error']['Message'])
            else:
                logger.info('Aggregated email sent! Message ID: %s.', response['MessageId'])
                start_warnings = datetime.now()
                warnings = []
        if len(sent_emails) > 0 and \
                (datetime.now() - max(sent_emails)).seconds > PERIOD:
            sent_emails = []

        # Grab the recent errors from the log files
        missing_logs_global = []
        unexpected_errors_global = []
        for f_name in LOG_FILES:
            f_name = 'logs/' + f_name
            # Read last 5 lines of a log file
            lines = os.popen(f'tail -n 5 {f_name}').read().split('\n')
            t = datetime.now()
            t_1 = t - timedelta(minutes=1)
            has_missing_logs = True
            has_unexpected_errors = False
            unexpected_errors = []
            for line in lines:
                # Check if there was activity for the last minute
                if t.strftime('%Y-%m-%d %H:%M') in line or t_1.strftime('%Y-%m-%d %H:%M') in line:
                    has_missing_logs = False
                if 'ERROR' in line:
                    if aggregated_conditions(line):
                        aggregated.append(line)
                    else:
                        has_unexpected_errors = True
                        unexpected_errors.append(line)
                elif 'WARNING' in line:
                    warnings.append(line)
            if has_missing_logs:
                missing_logs_global.append(body_text_lag(f_name))
            if has_unexpected_errors:
                unexpected_errors_global.extend(unexpected_errors)

        # sent_emails, logger are taken from global env
        def email_messages(messages, messages_old, title):
            # Check if the some of the messages were already emailed
            messages = [message for message in messages if message not in messages_old]
            if len(messages) > 0:
                if len(sent_emails) < MAX_PER_PERIOD:
                    try:
                        response = send_email(messages, title)
                        messages_old.extend(messages)
                        if len(messages_old) > OLD_BUFFER:
                            messages_old = messages_old[-OLD_BUFFER:]
                    except ClientError as e:
                        logger.error(e.response['Error']['Message'])
                    else:
                        logger.info('Email sent! Message ID: %s.', response['MessageId'])
                        sent_emails.append(datetime.now())
                else:
                    logger.warning('Will not send the email (too many per hour).')
            else:
                logger.info(f'No {title.lower()}.')
            return messages_old

        missing_logs_old = email_messages(
            missing_logs_global, missing_logs_old, 'Missing logs')
        unexpected_errors_old = email_messages(
            unexpected_errors_global, unexpected_errors_old, 'Unexpected errors')

        t = datetime.utcnow()
        sleeptime = 60 - (t.second + t.microsecond/1000000.0)
        time.sleep(sleeptime)
