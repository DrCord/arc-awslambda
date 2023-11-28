#! /usr/bin/env python
"""
    Name:
        grafana_reprovision_vehicle_groups.py
    Category:
        This file is part of AWSLambda.
    Purpose:
        Reprovision the Grafana vehicle group page in the specified environment.
    Usage (for dev):
        > ./grafana_reprovision_vehicle_groups.py
"""
import argparse
import boto3
import cognito
import json
import logging

client = boto3.client('lambda', 'us-west-2')

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

parser = argparse.ArgumentParser(description='receive command line arguments')
parser.add_argument('--env',
                    choices=['dev', 'staging', 'prod'],
                    help='provide the name of the stage/environment')
parser.add_argument('--user', default=None, help='authenticate as a specific user before invoking')


args = parser.parse_args()
env = args.env
user = args.user


def reprovision_groups(env, token):
    payload = {}
    if token is not None:
        payload['params'] = {
            "header": {
                "Authorization": token
            }
        }
        try:
            client.invoke(
                FunctionName=f'provision_grafana_groups:{env}',
                InvocationType='RequestResponse',
                LogType='Tail',
                Payload=json.dumps(payload)
            )
        except Exception as e:
            logger.error(f'Function provision_grafana_groups failed: {e}')
            raise e
        logger.info(f'Done reprovisioning groups for environment {env}')
    else:
        logger.info(f'Unable to authenticate before invoking lambdas')


def user_get_token(user):
    token = None
    if user is not None:
        token = cognito.authenticate(user)
    return token


def reprovision_vehicle_groups():
    logger.info(f'Starting reprovision of vehicle group dashboards for {env} ENV')
    token = user_get_token(user)
    reprovision_groups(env, token)
    logger.info(f'Reprovision of vehicle group dashboards for {env} ENV complete')


###############################################################################
# execution

if __name__ == '__main__':
    reprovision_vehicle_groups()
