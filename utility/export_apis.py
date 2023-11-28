import boto3
import argparse
import json
import os
import logging

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# argparse settings and results
parser = argparse.ArgumentParser(description='Export AWS API Gateways to swagger files for backup in version control')
parser.add_argument('--api_names',
                    nargs='+',
                    choices=[
                        'authorityManager',
                        'orders'
                        'palantir',
                        'recallsPublic',
                        'reef',
                        'statistics',
                        'userManager',
                        'vehicleManager',
                        'web'
                    ],
                    help='provide the name(s) of the API(s) to be exported')
parser.add_argument('--stage_names',
                    nargs='+',
                    choices=['dev', 'staging', 'prod'],
                    help='provide the names of the stage/environment')

args = parser.parse_args()
api_names = args.api_names
stage_names = args.stage_names


def reset_script_path():
    # sets base path of script to repo root then api-exports
    abspath = os.path.abspath(__file__)
    dname = os.path.dirname(abspath)
    os.chdir(dname)
    os.chdir('../api-exports')
    cwd = os.getcwd()


def export_api(api_name, stage_name):
    logger.info(f'Exporting API: {api_name}, stage: {stage_name} to file.')
    os.chdir(api_name)

    response = client.get_export(
        restApiId=API_IDS[api_name],
        stageName=stage_name,
        exportType='swagger',
        accepts='application/json',
        parameters={
            'extensions': 'apigateway'
        }
    )

    http_meta_data = response.get('ResponseMetadata', None)
    if http_meta_data is None:
        raise Exception("boto3 reponse does not include ResponseMetadata")

    http_status_code = http_meta_data.get('HTTPStatusCode', None)
    if http_status_code is None:
        raise Exception("boto3 ResponseMetadata does not include HTTPStatusCode")
    if http_status_code != 200:
        raise Exception("HTTPStatusCode {}".format(http_status_code))

    response_body_stream = response.get('body', None)
    if response_body_stream is None:
        raise Exception("boto3 response.body not set")

    response_body = json.loads(response_body_stream.read())

    # save file
    with open(f'{api_name}-api.{stage_name}.json', 'w') as outfile:
        json.dump(response_body, outfile, sort_keys=True, indent=2)
    # move back to api-exports folder for possible next export
    os.chdir('..')


# do stuff
API_IDS = {
    'authorityManager': '8xlss9lsy0',
    'orders': 'twbx26sw44',
    'fueLoyal': 'qr0ldv7ga9',
    'palantir': '1zmqntj0nd',
    'recallsPublic': '05zdqtma8k',
    'reef': 'c4sbssekn3',
    'statistics': 'blf3lokt20',
    'userManager': 'fq1v0dj83b',
    'vehicleManager': 'dsbyqxkezg',
    'web': 'kwqcd40pvl'
}
client = boto3.client('apigateway')

reset_script_path()

for api_name in api_names:
    for stage_name in stage_names:
        export_api(api_name, stage_name)
