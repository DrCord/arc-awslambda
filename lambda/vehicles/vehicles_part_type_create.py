import logging

from arcimoto.exceptions import *
import arcimoto.args
import arcimoto.db
import arcimoto.runtime
import arcimoto.user

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

arcimoto.args.register({
    'part_type': {
        'type': 'string',
        'required': True
    }
})


@arcimoto.runtime.handler
@arcimoto.user.require('model.write')
@arcimoto.db.transaction
def vehicles_part_type_create(part_type):
    global logger

    cursor = arcimoto.db.get_cursor()

    query = (
        'INSERT INTO vehicle_part_types '
        'VALUES (%s)'
    )

    cursor.execute(query, [part_type])
    return {}


lambda_handler = vehicles_part_type_create
