import logging
import boto3

import arcimoto.runtime

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

REEF_VEHICLE_GROUP_ID = 8


def managed_session_end(vin, test_runner_user_admin=True):
    args = {
        'vin': vin
    }
    return arcimoto.runtime.test_invoke_lambda('reef_managed_session_end', args, test_runner_user_admin)


def managed_session_get(id=None, vin=None, test_runner_user_admin=True):
    args = {}
    if id is not None:
        args['id'] = id
    if vin is not None:
        args['vin'] = vin
    return arcimoto.runtime.test_invoke_lambda('reef_managed_session_get', args, test_runner_user_admin)


def managed_session_list(test_runner_user_admin=True):
    return arcimoto.runtime.test_invoke_lambda('reef_managed_session_list', {}, test_runner_user_admin)


# this is used to setup vehicles for this package but not part of it
def managed_session_mode_set(vin, managed_session_mode=None):
    args = {
        'vin': vin
    }
    if managed_session_mode is not None:
        args['managed_session_mode'] = managed_session_mode
    return arcimoto.runtime.test_invoke_lambda('managed_session_mode_set', args, True)


def managed_session_start(vin, verification_id, test_runner_user_admin=True):
    args = {
        'vin': vin,
        'verification_id': verification_id
    }
    return arcimoto.runtime.test_invoke_lambda('reef_managed_session_start', args, test_runner_user_admin)


def managed_session_telemetry_get(id, test_runner_user_admin=True):
    args = {
        'managed_session_id': id
    }
    return arcimoto.runtime.test_invoke_lambda('reef_managed_session_telemetry_get', args, test_runner_user_admin)


def verify_dl(args, test_runner_user_admin=True):
    return arcimoto.runtime.test_invoke_lambda('reef_sheer_id_verify_dl', args, test_runner_user_admin)


def vehicle_shadow_synchronized(vin, test_runner_user_admin=True):
    args = {
        'vin': vin
    }
    return arcimoto.runtime.test_invoke_lambda('reef_vehicle_shadow_synchronized', args, test_runner_user_admin)


def managed_sessions_get_highest_id():
    managed_sessions = managed_session_list().get('managed_sessions', [])
    return managed_sessions[-1].get('id', 0)


@arcimoto.db.transaction
def add_invalid_vin_directly_to_vehicle_group(invalid_allowed_vin):
    cursor = arcimoto.db.get_cursor()

    query = (
        'INSERT INTO vehicle_join_vehicle_group (vin, group_id) '
        'VALUES (%s, %s)'
    )
    cursor.execute(query, [invalid_allowed_vin, REEF_VEHICLE_GROUP_ID])


@arcimoto.db.transaction
def remove_invalid_vin_directly_from_vehicle_group(invalid_allowed_vin):
    cursor = arcimoto.db.get_cursor()

    query = (
        'DELETE FROM vehicle_join_vehicle_group '
        'WHERE vin = %s'
    )
    cursor.execute(query, [invalid_allowed_vin])
