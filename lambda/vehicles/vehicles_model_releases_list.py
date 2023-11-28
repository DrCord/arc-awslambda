import logging

from arcimoto.exceptions import *
import arcimoto.runtime
import arcimoto.args
import arcimoto.user
import arcimoto.db

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

arcimoto.args.register({
    'model_id': {
        'type': 'integer',
        'nullable': True,
        'default': None,
        'min': 1
    }
})


@arcimoto.runtime.handler
@arcimoto.user.require('vehicles.vehicle.read')
def vehicles_model_releases_list(model_id):
    global logger

    cursor = arcimoto.db.get_cursor()

    query = (
        'SELECT '
        'vmr.model_release_id, '
        'vmr.description AS model_release_description, '
        'vmr.created, '
        'vm.model_name '
        'FROM vehicle_model_release vmr '
        'JOIN vehicle_model vm ON vm.id = vmr.model_id '
    )
    if model_id is not None:
        query += 'WHERE vmr.model_id = %s '

    query += 'ORDER BY vmr.model_release_id ASC'

    model_releases = []

    cursor.execute(query, [model_id])
    for record in cursor:
        model_releases.append(
            {
                'model_release_id': record['model_release_id'],
                'model_release_description': record['model_release_description'],
                'created': arcimoto.db.datetime_record_output(record['created']),
                'model_name': record['model_name']
            }
        )
    model_release_query = (
        'SELECT part_type, part_number '
        'FROM vehicle_model_parts '
        'WHERE model_release_id = %s'
    )

    for model_release in model_releases:
        model_release['parts'] = []
        cursor.execute(model_release_query, [model_release.get('model_release_id')])
        for record in cursor:
            model_release['parts'].append({
                'part_type': record['part_type'],
                'part_number': record['part_number']
            })

    return {'model_releases': model_releases}


lambda_handler = vehicles_model_releases_list
