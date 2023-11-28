import logging
import boto3

import arcimoto.runtime

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


def firmware_get_commit_info(args, test_runner_user_admin=True):
    return arcimoto.runtime.test_invoke_lambda('get_commit_info', args, test_runner_user_admin)


def firmware_version_get(args, test_runner_user_admin=True):
    return arcimoto.runtime.test_invoke_lambda('firmware_version_get', args, test_runner_user_admin).get('firmware', None)


def firmware_version_get_release_data(repo, test_runner_user_admin=True):
    return arcimoto.runtime.test_invoke_lambda('firmware_version_get_release_data', {'repo': repo}, test_runner_user_admin)


def firmware_version_refresh(test_runner_user_admin=True):
    return arcimoto.runtime.test_invoke_lambda('firmware_version_refresh', {}, test_runner_user_admin)


def firmware_version_set_release_data(args, test_runner_user_admin=True):
    return arcimoto.runtime.test_invoke_lambda('firmware_version_set_release_data', args, test_runner_user_admin).get('updated_firmware', None)


def firmware_version_vin_get(vin, test_runner_user_admin=True):
    return arcimoto.runtime.test_invoke_lambda('firmware_version_vin_get', {'vin': vin}, test_runner_user_admin)


def firmware_version_vin_set(args, test_runner_user_admin=True):
    return arcimoto.runtime.test_invoke_lambda('firmware_version_vin_set', args, test_runner_user_admin)
