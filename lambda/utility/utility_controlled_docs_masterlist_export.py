import boto3
import csv
from google.oauth2 import service_account
import gspread
import json
import logging
import re

from arcimoto.exceptions import *
import arcimoto.args
import arcimoto.runtime

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


@arcimoto.runtime.handler
def utility_controlled_docs_masterlist_export():
    domain = 'arcimoto.com'
    user = 'intranet-automation'
    key_file = arcimoto.runtime.get_secret('controlled_docs_masterlist_export.credentials')
    with open('/tmp/key_file.json', 'w') as f:
        json.dump(key_file, f)

    scope = ['https://www.googleapis.com/auth/drive']
    subject = '@'.join([user, domain])

    try:
        delegated_credentials = service_account.Credentials.from_service_account_file(
            '/tmp/key_file.json',
            scopes=scope,
            subject=subject
        )
    except Exception as e:
        raise ArcimotoAlertException(f'google: service account delegation failed: {e.args[0]}')

    try:
        client = gspread.authorize(delegated_credentials)
    except Exception as e:
        raise ArcimotoAlertException(f'gspread: authorization failed: {e.args[0]}')

    # Open Q40003 Documentation Log Sheet
    # https://docs.google.com/spreadsheets/d/1duKYNxvR0ljPmZ4apGuKE-Cweb1-NrK1y_qNCmS-cGs/
    try:
        sheet = client.open_by_key("1duKYNxvR0ljPmZ4apGuKE-Cweb1-NrK1y_qNCmS-cGs")
    except Exception as e:
        raise ArcimotoAlertException(f'gspread: unable to open file: {e.args[0]}')

    worksheet_list = sheet.worksheets()

    if arcimoto.runtime.get_env() == 'prod':
        s3_bucket = 'arcimoto-doc-control'
    else:
        s3_bucket = 'arcimoto-doc-control-test'

    s3 = boto3.client('s3')
    # Loop through each worksheet of the Documentation Log Sheet, generate a csv 
    # (unless it's an ignored sheet), and upload it to S3.
    for sheet in worksheet_list:
        if sheet.title not in ['Drop Down Menus Setup', 'Obsolete']:
            file_name = re.sub(r'\ \(\w+\)', '', sheet.title + ".csv")
            file_name = re.sub('/', '_', file_name)
            file_path = '/tmp/' + file_name
            with open(file_path, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerows(sheet.get_all_values())
            try:
                s3.upload_file(file_path, s3_bucket, file_name)
            except Exception as e:
                raise ArcimotoException(f'Uploading file, {file_name}, to S3 failed: {e.args[0]}')
    return {}


lambda_handler = utility_controlled_docs_masterlist_export
