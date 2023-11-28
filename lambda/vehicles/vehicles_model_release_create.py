import logging

from arcimoto.exceptions import *
import arcimoto.args
import arcimoto.db
import arcimoto.runtime
import arcimoto.user

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

part_types = [
    'BMS',
    'Charger',
    'Comm',
    'Display',
    'EPSU',
    'H Bridge',
    'Inverter - Left',
    'Inverter - Right',
    'IO Front',
    'IO Rear',
    'KERS Sensor',
    'LV',
    'VCU'
]

arcimoto.args.register({
    'model_id': {
        'type': 'integer',
        'required': True,
        'min': 1
    },
    'description': {
        'type': 'string',
        'required': True,
        'empty': False
    },
    'parts': {
        'type': 'dict',
        'required': True,
        'empty': False,
        'allowed': part_types,
        'contains': part_types
    }
})


@arcimoto.runtime.handler
@arcimoto.user.require('model.write')
@arcimoto.db.transaction
def vehicles_model_release_create(model_id, description, parts):
    global logger

    cursor = arcimoto.db.get_cursor()

    # check if model exists
    model_query = (
        'SELECT EXISTS (SELECT id '
        'FROM vehicle_model '
        'WHERE id = %s)'
    )
    cursor.execute(model_query, [model_id])
    result = cursor.fetchone()
    if not result[0]:
        raise ArcimotoArgumentError(f'Input validation failed: model_id {model_id} does not exist')

    # check if combo already exists for model
    models_query = (
        'SELECT model_release_id '
        'FROM vehicle_model_release '
        'WHERE model_id = %s'
    )
    cursor.execute(models_query, [model_id])
    model_model_release_ids = []
    for record in cursor.fetchall():
        model_model_release_ids.append(record['model_release_id'])

    vehicle_model_parts_query = (
        'SELECT model_release_id '
        'FROM vehicle_model_parts '
        'WHERE model_release_id IN %s '
        'AND '
    )
    parts_combination_model_releases = []
    first = True
    # loop and compare to previous itterations of part model releases for model_id
    # find if there are duplicate model release part configs for the model_id
    for part_type in part_types:
        part_model_releases = []
        query = vehicle_model_parts_query + f'part_type = %s AND part_number = %s'
        args = [tuple(model_model_release_ids), part_type, parts.get(part_type)]
        cursor.execute(query, args)
        for record in cursor.fetchall():
            part_model_releases.append(record['model_release_id'])
        if first:
            parts_combination_model_releases = part_model_releases
            first = False
        else:
            parts_combination_model_releases = set(parts_combination_model_releases) & set(part_model_releases)
    if len(parts_combination_model_releases):
        raise ArcimotoArgumentError(f'Input validation failed: parts configuration already exists for model id {model_id} as model release id {next(iter(parts_combination_model_releases))}')

    # insert data
    vehicle_model_release_query = (
        'INSERT INTO vehicle_model_release '
        '(description, model_id) VALUES (%s, %s) '
        'RETURNING model_release_id'
    )
    cursor.execute(vehicle_model_release_query, [description, model_id])
    result = cursor.fetchone()
    model_release_id = result.get('model_release_id', None)
    if model_release_id is None:
        raise ArcimotoException('Unable to create model release, no model release id returned from query.')

    vehicle_model_parts_query = (
        'INSERT INTO vehicle_model_parts '
        '(model_release_id, part_type, part_number) '
        'VALUES (%s, %s, %s)'
    )

    for part_type, part_number in parts.items():
        cursor.execute(vehicle_model_parts_query, [model_release_id, part_type, part_number])

    return {
        'model_release_id': model_release_id
    }


lambda_handler = vehicles_model_release_create
