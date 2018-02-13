import datetime
import time
import boto3
import os
from time import sleep

log_groups = os.environ['LOG_GROUP'].split(',')
s3_bucket_name = os.environ['BUCKET_NAME']


def from_timestamp():
    today = datetime.date.today()
    yesterday = datetime.datetime.combine(today - datetime.timedelta(days = 1), datetime.time(0, 0, 0))
    timestamp = time.mktime(yesterday.timetuple())
    return int(timestamp)

def to_timestamp(from_ts):
    return from_ts + (60 * 60 * 24) - 1

def lambda_handler(event, context):
    from_ts = from_timestamp()
    to_ts = to_timestamp(from_ts)
    client = boto3.client('logs')

    for log_group in log_groups:
        s3_prefix = log_group + '/%s' % (datetime.date.today() - datetime.timedelta(days = 1))
        try:
            client.create_export_task(
                logGroupName      = log_group,
                fromTime          = from_ts * 1000,
                to                = to_ts * 1000,
                destination       = s3_bucket_name,
                destinationPrefix = log_group
            )
            sleep(10)
        except Exception as e:
            print (e)

