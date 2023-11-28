#! /usr/bin/env python
"""
    Name:
        grafana_reprovision_vehicle_overviews.py
    Category:
        This file is part of AWSLambda.
    Purpose:
        Reprovision all Grafana vehicle group overview dashboards in the specified environment.
    Usage (for dev):
        > ./grafana_reprovision_group_overviews.py
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


def get_group_list(env, token):
    # run list vehicle groups lambda
    payload = {}
    if token is not None:
        payload['params'] = {
            "header": {
                "Authorization": token
            }
        }
    try:
        response = client.invoke(
            FunctionName='list_vehicle_groups:{}'.format(env),
            InvocationType='RequestResponse',
            LogType='Tail',
            Payload=json.dumps(payload)
        )
    except Exception as e:
        logger.error(f'Function list_vehicle_groups failed: {e}')
        raise e

    # parse response to json
    data = response['Payload'].read()
    jdata = json.loads(data)
    logger.info(f"Fleets list retrieved successfully")

    # iterate json and reducing to array of IDs
    group_id_list = []
    for group in jdata:
        group_id_list.append(group['id'])

    return group_id_list


def reprovision_overviews(group_id_list, env, token):
    payload = {}
    if token is not None:
        payload['params'] = {
            "header": {
                "Authorization": token
            }
        }
        fleets_count = len(group_id_list)
        count = 1
        for group_id in group_id_list:
            payload['group_id'] = group_id
            try:
                client.invoke(
                    FunctionName=f'provision_grafana_overview:{env}',
                    InvocationType='RequestResponse',
                    LogType='Tail',
                    Payload=json.dumps(payload)
                )
            except Exception as e:
                logger.error(f'Function provision_grafana_overview for group {group_id} failed: {e}')
                raise e
            logger.info(f'Done reprovisioning dashboard for group {group_id}. {count}/{fleets_count}')
            count += 1
    else:
        logger.info(f'Unable to authenticate before invoking lambdas')


def user_get_token(user):
    token = None
    if user is not None:
        token = cognito.authenticate(user)
    return token


def reprovision_group_overviews():
    logger.info(f'Starting reprovision of group overviews for {env} ENV')
    token = user_get_token(user)
    group_list = get_group_list(env, token)
    logger.info(f'group_list: {group_list}')
    reprovision_overviews(group_list, env, token)
    logger.info(f'Reprovision of group overviews complete for {env} ENV')


###############################################################################
# execution

if __name__ == '__main__':
    reprovision_group_overviews()
