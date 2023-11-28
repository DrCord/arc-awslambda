import logging
import boto3

import arcimoto.runtime

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


def add_vehicle_metadata(vin, section, data, test_runner_user_admin=True):
    args = {
        'vin': vin,
        'section': section,
        'data': data
    }
    return arcimoto.runtime.test_invoke_lambda('add_vehicle_metadata', args, test_runner_user_admin)


def model_release_create(model_id=None, description=None, parts=None, test_runner_user_admin=True):
    args = {}
    if model_id is not None:
        args['model_id'] = model_id
    if description is not None:
        args['description'] = description
    if parts is not None:
        args['parts'] = parts
    return arcimoto.runtime.test_invoke_lambda('vehicles_model_release_create', args, test_runner_user_admin)


def part_set(model_release_id=None, part_type=None, part_number=None, test_runner_user_admin=True):
    args = {}
    if model_release_id is not None:
        args['model_release_id'] = model_release_id
    if part_type is not None:
        args['part_type'] = part_type
    if part_number is not None:
        args['part_number'] = part_number
    return arcimoto.runtime.test_invoke_lambda('vehicles_model_release_part_set', args, test_runner_user_admin)


def part_type_create(part_type=None, test_runner_user_admin=True):
    args = {}
    if part_type is not None:
        args['part_type'] = part_type
    return arcimoto.runtime.test_invoke_lambda('vehicles_part_type_create', args, test_runner_user_admin)


def parts_get(model_release_id, test_runner_user_admin=True):
    return arcimoto.runtime.test_invoke_lambda('vehicles_model_release_parts_get', {'model_release_id': model_release_id}, test_runner_user_admin)


def get_telemetry_vehicle(vin, test_runner_user_admin=True):
    return arcimoto.runtime.test_invoke_lambda('get_telemetry_vehicle', {'vin': vin}, test_runner_user_admin)


def get_vehicle_shadow(vin, test_runner_user_admin=True):
    return arcimoto.runtime.test_invoke_lambda('get_vehicle_shadow', {'vin': vin}, test_runner_user_admin)


def provision_iot(vin, test_runner_user_admin=True):
    return arcimoto.runtime.test_invoke_lambda('provision_iot', {'vin': vin, 'thing_group': 'development'}, test_runner_user_admin)


def unprovision_iot(vin, test_runner_user_admin=True):
    return arcimoto.runtime.test_invoke_lambda('unprovision_iot', {'vin': vin}, test_runner_user_admin)


def provision_iot_certificate(vin, test_runner_user_admin=True):
    return arcimoto.runtime.test_invoke_lambda('provision_iot_certificate', {'vin': vin}, test_runner_user_admin)


def unprovision_iot_certificate(vin, test_runner_user_admin=True):
    return arcimoto.runtime.test_invoke_lambda('unprovision_iot_certificate', {'vin': vin}, test_runner_user_admin)


def provision_vehicle_telemetry(vin, model_release_id, test_runner_user_admin=True):
    return arcimoto.runtime.test_invoke_lambda('provision_vehicle_telemetry', {'vin': vin, 'model_release_id': model_release_id}, test_runner_user_admin)


def unprovision_vehicle_telemetry(vin, test_runner_user_admin=True):
    return arcimoto.runtime.test_invoke_lambda('unprovision_vehicle_telemetry', {'vin': vin}, test_runner_user_admin)


def update_shadow_document(vin):
    return arcimoto.runtime.invoke_lambda('update_shadow_document', {'vin': vin})


def gps_privacy_setting_get(vin, test_runner_user_admin=True):
    return arcimoto.runtime.test_invoke_lambda('gps_privacy_setting_get', {'vin': vin}, test_runner_user_admin)


def gps_recording_toggle(vin, record_gps, test_runner_user_admin=True):
    return arcimoto.runtime.test_invoke_lambda('gps_recording_toggle', {'vin': vin, 'record_gps': record_gps}, test_runner_user_admin)


def list_telemetry_vehicles(args={}, test_runner_user_admin=True):
    return arcimoto.runtime.test_invoke_lambda('list_telemetry_vehicles', args, test_runner_user_admin)


def register_vehicle(vin, data):
    args = {
        'vin': vin
    }
    if data is not None:
        args['data'] = data
    return arcimoto.runtime.invoke_lambda('register_vehicle', args)


def shadow_reported_state(vin, reported):
    args = {
        'vin': vin,
        'reported': reported
    }
    return arcimoto.runtime.invoke_lambda('shadow_reported_state', args)


def vehicle_part_install(vin=None, part_type=None, test_runner_user_admin=True):
    args = {}
    if vin is not None:
        args['vin'] = vin
    if part_type is not None:
        args['part_type'] = part_type
    return arcimoto.runtime.test_invoke_lambda('vehicles_vehicle_part_set', args, test_runner_user_admin)


def vehicles_options_set(vin=None, options=None, test_runner_user_admin=True):
    args = {}
    if vin is not None:
        args['vin'] = vin
    if options is not None:
        args['options'] = options
    return arcimoto.runtime.test_invoke_lambda('vehicles_options_set', args, test_runner_user_admin)


def vehicles_configuration_set(vin=None, configuration=None, test_runner_user_admin=True):
    args = {}
    if vin is not None:
        args['vin'] = vin
    if configuration is not None:
        args['configuration'] = configuration
    return arcimoto.runtime.test_invoke_lambda('vehicles_configuration_set', args, test_runner_user_admin)


def vehicle_shadow_synchronized(vin, test_runner_user_admin=True):
    args = {
        'vin': vin
    }
    return arcimoto.runtime.test_invoke_lambda('vehicles_vehicle_shadow_synchronized', args, test_runner_user_admin)


def vehicle_model_release_set(vin, model_release_id, test_runner_user_admin=True):
    return arcimoto.runtime.test_invoke_lambda('vehicles_vehicle_model_release_set', {'vin': vin, 'model_release_id': model_release_id}, test_runner_user_admin)


def firmware_components_list(test_runner_user_admin=True):
    return arcimoto.runtime.test_invoke_lambda('vehicles_firmware_components_list', {}, test_runner_user_admin)


def models_list(platform_id=None, test_runner_user_admin=True):
    return arcimoto.runtime.test_invoke_lambda('vehicles_models_list', {'platform_id': platform_id}, test_runner_user_admin)


def model_releases_list(model_id=None, test_runner_user_admin=True):
    return arcimoto.runtime.test_invoke_lambda('vehicles_model_releases_list', {'model_id': model_id}, test_runner_user_admin)
