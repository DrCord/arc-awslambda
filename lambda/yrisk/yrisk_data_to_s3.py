import logging
import json
import boto3
from botocore.exceptions import ClientError
from datetime import datetime

from arcimoto.exceptions import *
import arcimoto.runtime
import arcimoto.args
import arcimoto.user
import arcimoto.db

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

arcimoto.args.register({
    's3_bucket': {
        'type': 'string',
        'required': True,
        'empty': False
    },
    'json_data': {
        'type': 'dict',
        'required': True
    }
})

YRISK_ARCIMOTO_CLIENT_UUID = '9a4im0t0-36a1-41b5-92a0-ac660f76c37e'
YRISK_AWS_ROLE_ARN = 'arn:aws:iam::376428461977:role/external-yrisk-client-9a4im0t0-36a1-41b5-92a0-ac660f76c37e'


@arcimoto.runtime.handler
def yrisk_data_to_s3(s3_bucket, json_data):
    global logger

    # dump json to string
    data_string = json.dumps(json_data)

    # get date for filename
    try:
        current_month = datetime.now().month
        current_year = datetime.now().year
        last_month = current_month - 1 if current_month > 1 else 12
        last_month_year = current_year if current_month > 1 else current_year - 1
    except Exception as e:
        raise ArcimotoYRiskAlertException(f'Unable to get last month date info: {e}')

    # Send data to S3
    # send to arcimoto bucket for unit tests, dev, etc.
    if s3_bucket == 'arcimoto-yrisk':
        s3 = boto3.client('s3')
    else:
        # assume role to setup s3 connection
        sts_connection = boto3.client('sts')
        yrisk_acct = sts_connection.assume_role(
            RoleArn=YRISK_AWS_ROLE_ARN,
            RoleSessionName='arcimoto-yrisk-monthly-vehicle-data-dump'
        )

        try:
            ACCESS_KEY = yrisk_acct['Credentials']['AccessKeyId']
            SECRET_KEY = yrisk_acct['Credentials']['SecretAccessKey']
            SESSION_TOKEN = yrisk_acct['Credentials']['SessionToken']
        except Exception as e:
            raise ArcimotoYRiskAlertException(f'Unable to assume role via STS: {e}')

        try:
            # create service client using the assumed role credentials, e.g. S3
            s3 = boto3.client(
                's3',
                aws_access_key_id=ACCESS_KEY,
                aws_secret_access_key=SECRET_KEY,
                aws_session_token=SESSION_TOKEN,
            )
        except Exception as e:
            raise ArcimotoYRiskAlertException(f'Unable to create s3 client with assumed role: {e}')

    encoded_data_string = data_string.encode('utf-8')

    env = arcimoto.runtime.get_env()
    if env is arcimoto.runtime.ENV_PROD:
        file_name = '{}_{}.json'.format(
            last_month_year,
            last_month
        )
    else:
        file_name = '{}_{}_{}.json'.format(
            last_month_year,
            last_month,
            env
        )
    s3_path = f'{YRISK_ARCIMOTO_CLIENT_UUID}/' + file_name

    response = None
    try:
        response = s3.put_object(
            ACL='bucket-owner-full-control',  # ACL requested by Y-Risk
            Bucket=s3_bucket,
            Key=s3_path,
            Body=encoded_data_string
        )
    except ClientError:
        logger.exception('Could not upload object to bucket.')
        raise
    except Exception as e:
        raise ArcimotoYRiskAlertException(e)

    return {}


lambda_handler = yrisk_data_to_s3
