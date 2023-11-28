#! /usr/bin/env python
"""
    Name:
        grafana_reprovision_vehicle_dashboards.py
    Category:
        This file is part of AWSLambda.
    Purpose:
        Reprovision all Grafana vehicle dashboards in the specified environment.
    Usage (for dev):
        > ./grafana_reprovision_vehicle_dashboards.py
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


def get_vin_list(env, token):
    payload = {}
    if token is not None:
        payload['params'] = {
            "header": {
                "Authorization": token
            }
        }
    # run list telemetry vehicles lambda
    try:
        response = client.invoke(
            FunctionName='list_telemetry_vehicles:{}'.format(env),
            InvocationType='RequestResponse',
            LogType='Tail',
            Payload=json.dumps(payload)
        )
    except Exception as e:
        logger.error(f'Function list_telemetry_vehicles failed: {e}')
        raise e

    # parse response to json
    data = response['Payload'].read()
    jdata = json.loads(data)
    logger.info('Vehicles list retrieved successfully')

    # iterate json and reducing to array of vins
    vin_list = []
    for vehicle in jdata.get('vehicles'):
        vin_list.append(vehicle['vin'])

    return vin_list


def reprovision_dashboards(vin_list, env, token):
    payload = {}
    if token is not None:
        payload['params'] = {
            "header": {
                "Authorization": token
            }
        }
        vins_count = len(vin_list)
        count = 1
        for vin in vin_list:
            payload['vin'] = vin
            try:
                response = client.invoke(
                    FunctionName=f'provision_grafana_vehicle:{env}',
                    InvocationType='RequestResponse',
                    LogType='Tail',
                    Payload=json.dumps(payload)
                )
            except Exception as e:
                logger.error(f'Function provision_grafana_vehicle for VIN {vin} failed: {e}')
                raise e
            logger.info(f'Done reprovisioning dashboard for VIN {vin}. {count}/{vins_count}')
            count += 1
    else:
        logger.info(f'Unable to authenticate before invoking lambdas')


def user_get_token(user):
    token = None
    if user is not None:
        token = cognito.authenticate(user)
    return token


def reprovision_vehicle_dashboards():
    logger.info(f'Starting reprovision of vehicle dashboards for {env} ENV')
    token = user_get_token(user)
    vin_list = get_vin_list(env, token)
    reprovision_dashboards(vin_list, env, token)
    logger.info(f'Reprovision of vehicle dashboards for {env} ENV complete')


###############################################################################
# execution

if __name__ == '__main__':
    reprovision_vehicle_dashboards()
