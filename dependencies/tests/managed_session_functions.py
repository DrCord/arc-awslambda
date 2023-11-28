import logging
import boto3

import arcimoto.runtime

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


def end(vin, test_runner_user_admin=True):
    args = {
        'vin': vin
    }
    return arcimoto.runtime.test_invoke_lambda('managed_session_end', args, test_runner_user_admin)


def get(id=None, vin=None, test_runner_user_admin=True):
    args = {}
    if id is not None:
        args['id'] = id
    if vin is not None:
        args['vin'] = vin
    return arcimoto.runtime.test_invoke_lambda('managed_session_get', args, test_runner_user_admin)


def list(test_runner_user_admin=True):
    return arcimoto.runtime.test_invoke_lambda('managed_session_list', {}, test_runner_user_admin)


def mode_set(vin, managed_session_mode=None, test_runner_user_admin=True):
    args = {
        'vin': vin
    }
    if managed_session_mode is not None:
        args['managed_session_mode'] = managed_session_mode
    return arcimoto.runtime.test_invoke_lambda('managed_session_mode_set', args, test_runner_user_admin)


def start(vin, verification_id, pin=None, test_runner_user_admin=True):
    args = {
        'vin': vin,
        'verification_id': verification_id
    }
    if pin is not None:
        args['pin'] = pin
    return arcimoto.runtime.test_invoke_lambda('managed_session_start', args, test_runner_user_admin)


def telemetry_get(id, test_runner_user_admin=True):
    args = {
        'managed_session_id': id
    }
    return arcimoto.runtime.test_invoke_lambda('managed_session_telemetry_get', args, test_runner_user_admin)


def managed_sessions_get_highest_id():
    managed_sessions = list().get('managed_sessions', [])
    return managed_sessions[-1].get('id', 0)
