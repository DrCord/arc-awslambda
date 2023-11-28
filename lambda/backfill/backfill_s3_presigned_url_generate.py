import logging
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
@arcimoto.user.require('telemetry.backfill.engineering')
def backfill_s3_presigned_url_generate(file_name):
    global logger, BUCKET_NAME

    # generate and return S3 signed url to arcimoto-backfill bucket
    presigned_url = create_presigned_post(BUCKET_NAME, file_name)

    return {
        'presigned_url': presigned_url
    }


def create_presigned_post(bucket_name, object_name,
                          fields=None, conditions=None, expiration=3600):
    """Generate a presigned URL S3 POST request to upload a file

    :param bucket_name: string
    :param object_name: string
    :param fields: Dictionary of prefilled form fields
    :param conditions: List of conditions to include in the policy
    :param expiration: Time in seconds for the presigned URL to remain valid
    :return: Dictionary with the following keys:
        url: URL to post to
        fields: Dictionary of form fields and values to submit with the POST
    :return: None if error.
    """

    # Generate a presigned S3 POST URL
    s3_client = boto3.client('s3')
    try:
        response = s3_client.generate_presigned_post(bucket_name,
                                                     object_name,
                                                     Fields=fields,
                                                     Conditions=conditions,
                                                     ExpiresIn=expiration)
    except ClientError as e:
        logging.error(e)
        return None

    # The response contains the presigned URL and required fields
    return response


lambda_handler = backfill_s3_presigned_url_generate
