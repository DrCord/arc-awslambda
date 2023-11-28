import logging
import boto3

import arcimoto.runtime

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


def data_s3_verify(s3_bucket=None, test_runner_user_admin=True):
    return arcimoto.runtime.test_invoke_lambda('yrisk_data_s3_verify', {'s3_bucket': s3_bucket}, test_runner_user_admin)


def data_to_s3(s3_bucket=None, json_data=None, test_runner_user_admin=True):
    return arcimoto.runtime.test_invoke_lambda('yrisk_data_to_s3', {'s3_bucket': s3_bucket, 'json_data': json_data}, test_runner_user_admin)


def fleets_list(test_runner_user_admin=True):
    return arcimoto.runtime.test_invoke_lambda('yrisk_fleets_list', {}, test_runner_user_admin)


def notify(args, test_runner_user_admin=True):
    return arcimoto.runtime.test_invoke_lambda('yrisk_notify', args, test_runner_user_admin)


def notify_email(test_runner_user_admin=True):
    return arcimoto.runtime.test_invoke_lambda('yrisk_notify_email', {}, test_runner_user_admin)


def output_assemble(args, test_runner_user_admin=True):
    return arcimoto.runtime.test_invoke_lambda('yrisk_output_assemble', args, test_runner_user_admin)


def vehicles_list(args, test_runner_user_admin=True):
    return arcimoto.runtime.test_invoke_lambda('yrisk_vehicles_list', args, test_runner_user_admin)


def vehicle_telemetry_get(vin=None, test_runner_user_admin=True):
    return arcimoto.runtime.test_invoke_lambda('yrisk_vehicle_telemetry_get', {'vin': vin}, test_runner_user_admin)
