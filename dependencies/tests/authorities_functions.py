import logging
import boto3

import arcimoto.runtime
import arcimoto.tests

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

ARCIMOTO_AUTHORITY_ID = 1


def authkey_vehicle_get(vin, test_runner_user_admin=True):
    return arcimoto.runtime.test_invoke_lambda('authkey_vehicle_get', {'vin': vin}, test_runner_user_admin)


def factory_pin_generate(vin, test_runner_user_admin=True):
    return arcimoto.runtime.test_invoke_lambda('factory_pin_generate', {'vin': vin}, test_runner_user_admin)


def factory_pin_keep_pin_generate(vin, preserve_pin, test_runner_user_admin=True):
    return arcimoto.runtime.test_invoke_lambda('factory_pin_generate', {'vin': vin, 'preserve_pin': preserve_pin}, test_runner_user_admin)


def provision_vehicle_authority(authority_id, vin, test_runner_user_admin=True):
    return arcimoto.runtime.test_invoke_lambda('provision_vehicle_authority', {'id': authority_id, 'vin': vin}, test_runner_user_admin)


def unprovision_vehicle_authority(authority_id, vin, test_runner_user_admin=True):
    return arcimoto.runtime.test_invoke_lambda('unprovision_vehicle_authority', {'id': authority_id, 'vin': vin}, test_runner_user_admin)


def unprovision_vehicle_arcimoto_authority(vin, test_runner_user_admin=True):
    return arcimoto.runtime.test_invoke_lambda('unprovision_vehicle_arcimoto_authority', {'vin': vin}, test_runner_user_admin)


def create_authority(description='Unit Tester', parent_authority_id=None, use_default_kms_cmk=None, test_runner_user_admin=True):
    args = {
        'description': description
    }
    if parent_authority_id is not None:
        args['parent_authority_id'] = parent_authority_id
    if use_default_kms_cmk is not None:
        args['use_default_kms_cmk'] = use_default_kms_cmk
    return arcimoto.runtime.test_invoke_lambda('create_authority', args, test_runner_user_admin)


def delete_authority(authority_id, test_runner_user_admin=True):
    return arcimoto.runtime.test_invoke_lambda('delete_authority', {'id': authority_id}, test_runner_user_admin)


def rekey_authority(authority_id, test_runner_user_admin=True):
    return arcimoto.runtime.test_invoke_lambda('rekey_authority', {'id': authority_id}, test_runner_user_admin)


def sign_vehicle_token(authority_id, token, test_runner_user_admin=True):
    return arcimoto.runtime.test_invoke_lambda('sign_vehicle_token', {'id': authority_id, 'token': token}, test_runner_user_admin)


def get_authority(authority_id, test_runner_user_admin=True):
    return arcimoto.runtime.test_invoke_lambda('get_authority', {'id': authority_id}, test_runner_user_admin)


def list_authorities(filter_args=None, include_vin=None, test_runner_user_admin=True):
    args = {}
    if filter_args is not None or include_vin is not None:
        args['params'] = {
            'querystring': {}
        }
        if filter_args is not None:
            args['params']['querystring']['filter_args'] = filter_args
        if include_vin is not None:
            args['params']['querystring']['include_vin'] = include_vin
    return arcimoto.runtime.test_invoke_lambda('list_authorities', args, test_runner_user_admin)


def authorities_highest_id():
    return list_authorities()[-1].get('id', 1)


def get_trusted_keys(vin, test_runner_user_admin=True):
    return arcimoto.runtime.test_invoke_lambda('get_trusted_keys', {'vin': vin}, test_runner_user_admin)


def list_vehicles(filter_args=None, test_runner_user_admin=True):
    args = {}
    if filter_args is not None:
        args['filter_args'] = filter_args
    return arcimoto.runtime.test_invoke_lambda('list_vehicles', args, test_runner_user_admin)
