import logging

from arcimoto.exceptions import *
import arcimoto.runtime
import arcimoto.args
import arcimoto.user
import arcimoto.db

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

arcimoto.args.register({
    'fleets_db_data': {
        'type': 'dict'
    }
})


@arcimoto.runtime.handler
def yrisk_vehicles_list(fleets_db_data):
    global logger

    vehicle_groups = fleets_db_data.get('vehicle_groups', [])

    cursor = arcimoto.db.get_cursor()

    platform_id = 1

    query = (
        'SELECT model_name, letter_code '
        'FROM vehicle_model '
        'WHERE platform_id = %s'
    )
    models = []
    models_codes_map = {}
    cursor.execute(query, [platform_id])
    for record in cursor:
        models.append(
            {
                'model_name': record['model_name'],
                'letter_code': record['letter_code']
            }
        )
        models_codes_map[record['letter_code']] = record['model_name']

    env = arcimoto.runtime.get_env()

    if env == arcimoto.runtime.ENV_PROD:
        vin_model_position = 4
    elif env == arcimoto.runtime.ENV_STAGING:
        vin_model_position = 10
    elif env == arcimoto.runtime.ENV_DEV:
        vin_model_position = 8

    vehicle_query = (
        'SELECT '
        'v.vin as vin, '
        'l.location_name as location_name, '
        'COALESCE(l.city, \'None\')   as city, '
        'l.governing_district as governing_district, '
        'vgt.group_type as group_type, '
        'alc.code as location_code, '
        'adc.code as department_code '
        'FROM vehicle AS v '
        'JOIN vehicle_join_vehicle_group AS v_j_vg ON v.vin = v_j_vg.vin '
        'JOIN vehicle_group AS vg ON vg.id = v_j_vg.group_id '
        'JOIN vehicle_group_join_locations AS vg_j_l ON vg.id = vg_j_l.group_id '
        'JOIN locations as l ON vg_j_l.location_id = l.id '
        'JOIN vehicle_group_join_vehicle_group_type AS vg_j_vgt ON vg.id = vg_j_vgt.group_id '
        'JOIN vehicle_group_type AS vgt ON vg_j_vgt.type_id = vgt.id '
        'LEFT JOIN location_join_accounting_location_code as l_j_alc on l.id = l_j_alc.location_id '
        'LEFT JOIN accounting_location_code as alc on alc.id = l_j_alc.accounting_location_code_id '
        'LEFT JOIN vehicle_group_join_accounting_department_code as vg_j_adc on vg_j_adc.vehicle_group_id = vg.id '
        'LEFT JOIN public.accounting_department_code adc on adc.id = vg_j_adc.accounting_department_code_id '

        'WHERE v_j_vg.group_id IN %s '
        'ORDER BY v.vin'
    )
    vehicles = []
    cursor.execute(vehicle_query, [tuple(vehicle_groups)])
    for record in cursor:
        vin = record['vin']
        vehicles.append({
            'vin': vin,
            'location': {
                'name': record['location_name'],
                'city': record['city'],
                'state': record['governing_district'],
                'location_code': record['location_code']
            },
            'coverage': record['group_type'],
            'model': models_codes_map[vin[vin_model_position]],
            'department_code': record['department_code']
        })
    return {'vehicles': vehicles}


lambda_handler = yrisk_vehicles_list
