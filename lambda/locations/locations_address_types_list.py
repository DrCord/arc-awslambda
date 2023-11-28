import logging

from arcimoto.exceptions import *
import arcimoto.runtime
import arcimoto.db

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


@arcimoto.runtime.handler
def locations_address_types_list():
    '''List all address types, e.g. P.O Box, Suite, etc.'''
    global logger

    cursor = arcimoto.db.get_cursor()
    try:
        query = (
            'SELECT id, address_type '
            'FROM locations_address_types '
            'ORDER BY id ASC'
        )
        cursor.execute(query)

        result = []
        for record in cursor:
            result.append(
                {
                    'id': record['id'],
                    'address_type': record['address_type']
                }
            )
    except Exception as e:
        raise ArcimotoException(f'Unable to get address types from db: {e}') from e

    return {'address_types': result}


lambda_handler = locations_address_types_list
