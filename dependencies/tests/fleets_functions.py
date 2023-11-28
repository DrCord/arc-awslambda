import logging
import boto3

import arcimoto.runtime
import arcimoto.tests

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


def accounting_department_code_create(args, test_runner_user_admin=True):
    return arcimoto.runtime.test_invoke_lambda('fleets_accounting_department_code_create', args, test_runner_user_admin)


def accounting_department_code_delete(args, test_runner_user_admin=True):
    return arcimoto.runtime.test_invoke_lambda('fleets_accounting_department_code_delete', args, test_runner_user_admin)


def accounting_department_codes_list(test_runner_user_admin=True):
    return arcimoto.runtime.test_invoke_lambda('fleets_accounting_department_codes_list', {}, test_runner_user_admin)


def fleet_update(args, test_runner_user_admin=True):
    return arcimoto.runtime.test_invoke_lambda('fleets_fleet_update', args, test_runner_user_admin)


def vehicle_group_create(args=None, test_runner_user_admin=True):
    if args is None:
        args = {
            'group': 'Unit Test'
        }
    vehicle_group = arcimoto.runtime.test_invoke_lambda('create_vehicle_group', args, test_runner_user_admin)
    return vehicle_group.get('id', None)


def vehicle_group_delete(group_id, test_runner_user_admin=True):
    return arcimoto.runtime.test_invoke_lambda('delete_vehicle_group', {'group_id': group_id}, test_runner_user_admin)


def vehicle_group_add_user(group_id, username, test_runner_user_admin=True):
    return arcimoto.runtime.test_invoke_lambda('fleets_vehicle_group_add_user', {'vehicle_group_id': group_id, 'username': username}, test_runner_user_admin)


def vehicle_group_add_vehicle(group_id, vin, test_runner_user_admin=True):
    return arcimoto.runtime.test_invoke_lambda('add_vehicle_to_group', {'group_id': group_id, 'vin': vin}, test_runner_user_admin)


def user_groups_get(username, test_runner_user_admin=True):
    return arcimoto.runtime.test_invoke_lambda('user_groups_get', {'username': username}, test_runner_user_admin)


def vehicle_group_remove_vehicle(group_id, vin, test_runner_user_admin=True):
    return arcimoto.runtime.test_invoke_lambda('remove_vehicle_from_group', {'group_id': group_id, 'vin': vin}, test_runner_user_admin)


def vehicle_group_arcimoto_remove_vehicle(vin, test_runner_user_admin=True):
    return arcimoto.runtime.test_invoke_lambda('remove_vehicle_from_arcimoto_group', {'vin': vin}, test_runner_user_admin)


def vehicle_group_remove_user(group_id, username, test_runner_user_admin=True):
    return arcimoto.runtime.test_invoke_lambda('fleets_vehicle_group_remove_user', {'vehicle_group_id': group_id, 'username': username}, test_runner_user_admin)


def vehicle_group_get(group_id, test_runner_user_admin=True):
    return arcimoto.runtime.test_invoke_lambda('get_vehicle_group', {'group_id': group_id}, test_runner_user_admin)


def vehicle_groups_list(test_runner_user_admin=True):
    return arcimoto.runtime.test_invoke_lambda('list_vehicle_groups', {}, test_runner_user_admin)


def statistics_get(fleet_name, test_runner_user_admin=True):
    return arcimoto.runtime.test_invoke_lambda('fleets_statistics_get', {'fleet_name': fleet_name}, test_runner_user_admin)


def vehicle_group_accounting_department_code_set(args, test_runner_user_admin=True):
    return arcimoto.runtime.test_invoke_lambda('fleets_vehicle_group_accounting_department_code_set', args, test_runner_user_admin)


def vehicle_group_location_set(args, test_runner_user_admin=True):
    return arcimoto.runtime.test_invoke_lambda('fleets_vehicle_group_location_set', args, test_runner_user_admin)


def vehicle_group_type_set(args, test_runner_user_admin=True):
    return arcimoto.runtime.test_invoke_lambda('fleets_vehicle_group_type_set', args, test_runner_user_admin)


def vehicle_group_types_list(test_runner_user_admin=True):
    return arcimoto.runtime.test_invoke_lambda('fleets_vehicle_group_types_list', {}, test_runner_user_admin)
