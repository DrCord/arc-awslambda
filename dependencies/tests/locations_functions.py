import logging
import boto3

import arcimoto.runtime

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


def accounting_location_code_create(args, test_runner_user_admin=True):
    return arcimoto.runtime.test_invoke_lambda('locations_accounting_location_code_create', args, test_runner_user_admin)


def accounting_location_code_delete(args, test_runner_user_admin=True):
    return arcimoto.runtime.test_invoke_lambda('locations_accounting_location_code_delete', args, test_runner_user_admin)


def accounting_location_codes_list(test_runner_user_admin=True):
    return arcimoto.runtime.test_invoke_lambda('locations_accounting_location_codes_list', {}, test_runner_user_admin)


def address_types_list(test_runner_user_admin=True):
    return arcimoto.runtime.test_invoke_lambda('locations_address_types_list', {}, test_runner_user_admin)


def countries_list(test_runner_user_admin=True):
    return arcimoto.runtime.test_invoke_lambda('locations_countries_list', {}, test_runner_user_admin)


def location_create(args, test_runner_user_admin=True):
    return arcimoto.runtime.test_invoke_lambda('locations_location_create', args, test_runner_user_admin)


def location_delete(id=None, test_runner_user_admin=True):
    return arcimoto.runtime.test_invoke_lambda('locations_location_delete', {'id': id}, test_runner_user_admin)


def location_get(id=None, test_runner_user_admin=True):
    return arcimoto.runtime.test_invoke_lambda('locations_location_get', {'id': id}, test_runner_user_admin)


def location_update(args, test_runner_user_admin=True):
    return arcimoto.runtime.test_invoke_lambda('locations_location_update', args, test_runner_user_admin)


def location_accounting_location_code_set(args, test_runner_user_admin=True):
    return arcimoto.runtime.test_invoke_lambda('locations_location_accounting_location_code_set', args, test_runner_user_admin)


def locations_list(test_runner_user_admin=True):
    return arcimoto.runtime.test_invoke_lambda('locations_locations_list', {}, test_runner_user_admin)


def address_types_get_highest_id():
    address_types = address_types_list().get('address_types', [])
    return address_types[-1].get('id', 0)


def locations_get_highest_id():
    locations = locations_list().get('locations', [])
    return locations[-1].get('id', 0)
