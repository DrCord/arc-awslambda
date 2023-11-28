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
    },
    'file_length': {
        'type': 'integer',
        'required': True
    },
    'next_read_byte': {
        'type': 'integer',
        'default': 0
    }
})

BUCKET_NAME = 'arcimoto-backfill'
FILE_CHUNK_SIZE = 200000


@arcimoto.runtime.handler
def backfill_s3_upload_file(file_name, file_length, next_read_byte):
    global logger, BUCKET_NAME, FILE_CHUNK_SIZE

    if next_read_byte >= file_length:
        return {
            'atoms': [],
            'read_range': None,
            'next_iteration_read_byte': None
        }

    s3 = boto3.resource('s3')
    first_byte = next_read_byte
    last_byte = first_byte + FILE_CHUNK_SIZE if first_byte + FILE_CHUNK_SIZE <= file_length else file_length

    # body is too large to return and process with a state machine outright
    # so we chunk it up and process each chunk until complete
    read_range = f'bytes={first_byte}-{last_byte}'
    atoms = []

    try:
        obj = s3.Object(BUCKET_NAME, file_name)
        body = obj.get(Range=read_range)['Body'].read().decode()
    except ClientError:
        logger.exception('Could not get object from bucket.')
        raise
    except Exception as e:
        raise ArcimotoServiceAlertException(e)

    # split body into atoms
    items = body.splitlines()

    # throw away last atom if incomplete
    if items[-1][-1] != '}':
        # remove last atom's bytes from last_byte returned data
        last_item_byte_len = len(items[-1].encode('utf-8'))
        next_iteration_read_byte = last_byte - last_item_byte_len + 1
        items = items[:-1]
    else:
        next_iteration_read_byte = last_byte + 1

    for item in items:
        # ignore empty (bad) packets
        if item == '':
            logger.warn(f'Empty string is not valid JSON, ignoring packet')
            continue
        try:
            json_item = json.loads(item)
        except json.decoder.JSONDecodeError as e:
            # ignore bad packets
            logger.warn(f'JSONDecodeError: {e} -- item: {item}, ignoring packet')
            continue
        except Exception as e:
            raise ArcimotoServiceAlertException(f'Error: {e} -- item: {item}')

        atoms.append(json_item)

    return {
        'atoms': atoms,
        'read_range': read_range,
        'next_iteration_read_byte': next_iteration_read_byte
    }


lambda_handler = backfill_s3_upload_file
