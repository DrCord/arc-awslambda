import logging

from arcimoto.exceptions import *
import arcimoto.runtime
import arcimoto.user
import arcimoto.db

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

arcimoto.args.register({
    'id': {
        'type': 'integer',
        'required': True,
        'min': 1
    }
})


@arcimoto.runtime.handler
@arcimoto.user.require('locations.delete')
@arcimoto.db.transaction
def locations_location_delete(id):
    '''Delete location by id'''
    global logger

    cursor = arcimoto.db.get_cursor()

    try:
        # don't delete joins/references as they should be set to `ON CASCADE: DELETE/UPDATE`
        query = (
            'DELETE FROM locations '
            'WHERE id=%s'
        )
        cursor.execute(query, [id])
    except Exception as e:
        raise ArcimotoException(f'Unable to delete location with id {id}: {e}') from e

    return {}


lambda_handler = locations_location_delete
