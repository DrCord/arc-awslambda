import logging
import json
import base64
import boto3
from datetime import datetime
from botocore.exceptions import ClientError

from arcimoto.exceptions import *
import arcimoto.runtime
import arcimoto.args
import arcimoto.user

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

arcimoto.args.register({
    'file_name': {
        'type': 'string',
        'required': True
    }
})

BUCKET_NAME = 'arcimoto-backfill'


@arcimoto.runtime.handler
def backfill_s3_delete_file(file_name):
    global logger, BUCKET_NAME

    s3 = boto3.resource('s3')

    try:
        obj = s3.Object(BUCKET_NAME, file_name)
        response = obj.delete()
    except ClientError:
        logger.exception('Could not delete object from bucket.')
        raise
    except Exception as e:
        raise ArcimotoException(e)

    return {}


lambda_handler = backfill_s3_delete_file
