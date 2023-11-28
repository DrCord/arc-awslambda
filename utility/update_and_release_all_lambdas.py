import boto3
import json
import os
import logging
import argparse
import subprocess

logging.basicConfig()
logger = logging.getLogger(__name__)

DEPENDENCIES_CONFIG = 'dependencies.json'

# argparse settings and results
parser = argparse.ArgumentParser(description='Deploy a lambda function bundle to AWS')
parser.add_argument('--verbose', action='store_true', help='Output detailed progress')
args = parser.parse_args()

logger.setLevel(logging.DEBUG if args.verbose else logging.INFO)


def find_root_directory_path():
    path = os.path.abspath(os.path.dirname(__file__))
    while path != "/":
        if os.path.exists(os.path.join(path, DEPENDENCIES_CONFIG)):
            return path
        (path, current_dir) = os.path.split(path)


def get_lambda_names():
    lambda_names = []
    try:
        dependencies = {}
        with open(os.path.join(root_path, DEPENDENCIES_CONFIG)) as f:
            dependencies = json.load(f)

        functions = dependencies.get('functions', {})

        for key in functions.keys():
            lambda_names.append(key)

    except Exception as e:
        raise SystemExit(f'Failed to load function names from dependencies.json: {e}')

    return lambda_names


# setup root path
root_path = find_root_directory_path()

# get all lambda names
lambda_names = get_lambda_names()
logger.info('lambda names: ')
logger.info(lambda_names)

description = 'released to fix bug in db caching'
lambda_utility_path = os.path.join(root_path, 'utility/lambda')

for lambda_name in lambda_names:
    subprocess.call(f'python {lambda_utility_path} update {lambda_name}', shell=True)
    logger.info(f'Updated lambda {lambda_name} code')

    subprocess.call(f'python {lambda_utility_path} release {lambda_name} staging --description "{description}"', shell=True)
    logger.info(f'Released lambda {lambda_name} to staging')

    subprocess.call(f'python {lambda_utility_path} release {lambda_name} prod --description "{description}"', shell=True)
    logger.info(f'Released lambda {lambda_name} to prod')
