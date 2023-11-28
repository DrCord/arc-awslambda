import logging
import boto3
import base64
import json

from arcimoto.exceptions import *
import arcimoto.runtime
import arcimoto.args
import arcimoto.user
import arcimoto.db

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

arcimoto.args.register({
    'vin': {
        'type': 'string',
        'required': True
    }
})


@arcimoto.runtime.handler
def get_trusted_keys(vin):
    global logger

    cursor = arcimoto.db.get_cursor()
    query = (
        'SELECT a.public_key '
        'FROM vehicle_authority v '
        'LEFT JOIN authority_keys a '
        'ON v.authority_id=a.authority_keys_id '
        'WHERE v.vin=%s'
    )
    cursor.execute(query, (vin,))
    rows = cursor.fetchall()

    trust_list = []
    for row in rows:
        # convert the memoryview object returned from the query into local bytes
        key = bytes(row[0])
        # base64 convert the key, decoding as utf-8 string
        b64_key = base64.b64encode(key).decode('utf-8')
        # add it to the list
        trust_list.append(b64_key)

    return trust_list


lambda_handler = get_trusted_keys
