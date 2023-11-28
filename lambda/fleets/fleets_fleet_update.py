import logging

from arcimoto.exceptions import *
import arcimoto.runtime
import arcimoto.user
import arcimoto.db
import arcimoto.args

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

arcimoto.args.register({
    'id': {
        'type': 'integer',
        'required': True,
        'min': 1
    },
    'fleet_name': {
        'type': 'string',
        'required': True,
        'empty': False
    }
})


@arcimoto.runtime.handler
@arcimoto.user.require('fleets.group.write')
@arcimoto.db.transaction
def fleets_fleet_update(id, fleet_name):
    global logger

    cursor = arcimoto.db.get_cursor()

    try:
        where_predicates = [
            {
                'column': 'id',
                'operator': '=',
                'value': id
            }
        ]
        columns_data = [
            {'name': fleet_name}
        ]
        cursor.execute(
            *arcimoto.db.prepare_update_query_and_params(
                'vehicle_group',
                where_predicates,
                columns_data
            )
        )
        record = cursor.fetchone()

        output = {
            'id': record['id'],
            'fleet_name': record['name']
        }
    except Exception as e:
        raise ArcimotoException(f'Unable to update fleet record with id {id}: {e}') from e

    return output


lambda_handler = fleets_fleet_update
