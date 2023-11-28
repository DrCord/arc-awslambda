import logging
import boto3

import arcimoto.runtime

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


def add_telemetry_definition(metrics, test_runner_user_admin=True):
    return arcimoto.runtime.test_invoke_lambda('add_telemetry_definition', {'metrics': metrics}, test_runner_user_admin)


def get_telemetry_definition(vin):
    return arcimoto.runtime.invoke_lambda('get_telemetry_definition', {'vin': vin})


def set_telemetry_version(vin, version, test_runner_user_admin=True):
    return arcimoto.runtime.test_invoke_lambda('set_telemetry_version', {'vin': vin, 'version': version}, test_runner_user_admin)


def get_telemetry_metrics_keys(version=None, test_runner_user_admin=True):
    args = {}
    if version is not None:
        args['versionId'] = version
    return arcimoto.runtime.test_invoke_lambda('get_telemetry_metrics_keys', args, test_runner_user_admin)


def get_telemetry_points(vin, test_runner_user_admin=True):
    return arcimoto.runtime.test_invoke_lambda('get_telemetry_points', {'vin': vin}, test_runner_user_admin)


def set_telemetry_points(vin, telemetry_points, test_runner_user_admin=True):
    return arcimoto.runtime.test_invoke_lambda('set_telemetry_points', {'vin': vin, 'telemetry_points': telemetry_points}, test_runner_user_admin)


def telemetry_get_initial_version():
    return 'Lyahzs_tY1eaUJcPLaSJpwjfKoJZQOtI'


def telemetry_vpc_ingest_influx(args):
    return arcimoto.runtime.invoke_lambda('telemetry_vpc_ingest_influx', args)


def telemetry_ingest_timestream(args):
    return arcimoto.runtime.invoke_lambda('telemetry_ingest_timestream', args)


def telemetry_points_get_defaults(test_runner_user_admin=True):
    return arcimoto.runtime.test_invoke_lambda('telemetry_points_get_defaults', {}, test_runner_user_admin)


def telemetry_report_vehicles_overcharge():
    return arcimoto.runtime.test_invoke_lambda('telemetry_report_vehicles_overcharge', {}, True)


def telemetry_vehicles_timestream_get(vins, telemetry_points, test_runner_user_admin=True):
    args = {
        'vins': vins,
        'telemetry_points': telemetry_points
    }
    return arcimoto.runtime.test_invoke_lambda('telemetry_vehicles_timestream_get', args, test_runner_user_admin)


def unpack_telemetry_message(args):
    return arcimoto.runtime.invoke_lambda('unpack_telemetry_message', args)


def vehicles_telemetry_get(vins, telemetry_points, test_runner_user_admin=True):
    args = {
        'vins': vins,
        'telemetry_points': telemetry_points
    }
    return arcimoto.runtime.test_invoke_lambda('vehicles_telemetry_get', args, test_runner_user_admin)
