import logging

from arcimoto.exceptions import *
import arcimoto.runtime
import arcimoto.args
import arcimoto.user
import arcimoto.db

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

arcimoto.args.register({
    'platform_id': {
        'type': 'integer',
        'default': 1,
        'min': 1
    }
})


@arcimoto.runtime.handler
def vehicles_models_list(platform_id):
    global logger

    cursor = arcimoto.db.get_cursor()

    query = (
        'SELECT id, model_name, letter_code, description, created '
        'FROM vehicle_model '
        'WHERE platform_id = %s'
    )
    models = []

    cursor.execute(query, [platform_id])
    for record in cursor:
        models.append(
            {
                'id': record['id'],
                'model_name': record['model_name'],
                'letter_code': record['letter_code'],
                'description': record['description'],
                'created': arcimoto.db.datetime_record_output(record['created'])
            }
        )
    return {'models': models}


lambda_handler = vehicles_models_list
