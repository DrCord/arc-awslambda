import json
import boto3

import logging

from arcimoto.exceptions import *
import arcimoto.runtime
import arcimoto.user
import arcimoto.db

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

cwl = boto3.client('logs')


@arcimoto.runtime.handler
def utility_cwl_set_retention():

    '''
    Sets log retention for all cloudwatch log groups with a 'never expire' retention setting to 90 days.

    This is set to run monthly on the 1st via a ClouudWatch event:
    https://us-west-2.console.aws.amazon.com/events/home?region=us-west-2#/eventbus/default/rules/CloudWatch-Log-Groups-Set-Retention
    '''

    token = None
    defaultRetentionInDays = 90

    paginator = cwl.get_paginator('describe_log_groups')

    page_iterator = paginator.paginate(
        PaginationConfig={'PageSize': 10, 'StartingToken': token})

    for page in page_iterator:
        print("token ", token)

        for pg in page["logGroups"]:
            if 'retentionInDays' in pg:
                continue
            else:
                lgName = pg["logGroupName"]
                print(lgName)

                response = cwl.put_retention_policy(
                    logGroupName=lgName,
                    retentionInDays=defaultRetentionInDays
                )
        try:
            token = page["nextToken"]
        except KeyError:
            break

    body = {
        "message": "utility_cwl_set_retention Successful",
    }

    response = {
        "statusCode": 200,
        "body": json.dumps(body)
    }

    return response


lambda_handler = utility_cwl_set_retention
