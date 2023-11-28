import boto3
from botocore.exceptions import ClientError
import io
import json
import logging
import os
import requests
import tempfile
from zipfile import ZipFile

from arcimoto.exceptions import *
import arcimoto.runtime

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

arcimoto.args.register({
    'lambda_name': {
        'type': 'string',
        'required': True,
        'empty': False
    }
})

client = None


@arcimoto.runtime.handler
def unit_test_lambda_get_tests(lambda_name):
    global client, logger

    lambda_tests = []

    client = boto3.client('lambda')

    url = get_function_code_presigned_url(lambda_name)

    if url is not None:
        function_code_zip = get_function_code_zip_from_presigned_url(url)
        lambda_tests.extend(get_lambda_tests_from_bundle_json_in_zip(lambda_name, function_code_zip))

    # if no tests check if `test_{{LAMBDA_NAME}}` exists to handle lambdas without bundle.json available
    if len(lambda_tests) == 0 and lambda_default_test_exists(lambda_name):
        lambda_tests.append(f'test_{lambda_name}')

    return {
        'lambda_tests': lambda_tests
    }


def get_lambda_tests_from_bundle_json_in_zip(lambda_name, function_code_zip):
    lambda_tests = []
    # get bundle.json if available - extract the single file from zip
    with tempfile.TemporaryDirectory() as tmpdir:
        os.chdir(tmpdir)
        with ZipFile(io.BytesIO(function_code_zip.content), 'r') as zipObject:
            listOfFileNames = zipObject.namelist()
            for fileName in listOfFileNames:
                if fileName == 'bundle.json':
                    zipObject.extract(fileName)

        try:
            bundle_json = bundle_json_load(tmpdir)
            bundle_lambda_tests = bundle_json.get('lambdas', {}).get(lambda_name, {}).get('tests', [])
            lambda_tests.extend(bundle_lambda_tests)
        except Exception as e:
            logger.warning(f'Unable to get `bundle.json` for function {lambda_name}')
    return lambda_tests


def lambda_default_test_exists(lambda_name):
    default_test_name = f'test_{lambda_name}'
    default_test_exists = False
    # check if default test_ lambda exists
    try:
        client.get_function(FunctionName=default_test_name)
        default_test_exists = True
        logger.info(f'Default test {default_test_name} for {lambda_name} found')
    except ClientError as e:
        logger.warning(f'Default test {default_test_name} for {lambda_name} does not exist')

    return default_test_exists


def get_function_code_zip_from_presigned_url(url):
    get_function_code_response = None
    if url is not None:
        get_function_code_response = requests.get(url)

    return get_function_code_response


def get_function_code_presigned_url(lambda_name):
    url = None

    get_function_response = get_function(lambda_name)

    if get_function_response is not None:
        try:
            url = get_function_response['Code']['Location']
        except Exception as e:
            logger.warning(f'Unable to get S3 signed URL to get function {lambda_name} code')

    return url


def get_function(lambda_name):
    get_function_response = None

    try:
        get_function_response = client.get_function(FunctionName=lambda_name)
    except Exception as e:
        logger.warning(f'Unable to get function from AWS to check bundle.json for tests: {e}')

    return get_function_response


def bundle_json_load(tmpdir):
    f = open(f'{tmpdir}/bundle.json')
    bundle_json = json.load(f)
    f.close()

    return bundle_json


lambda_handler = unit_test_lambda_get_tests
