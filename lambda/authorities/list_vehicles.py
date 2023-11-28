import logging
import json

from arcimoto.exceptions import *
import arcimoto.runtime
import arcimoto.args
import arcimoto.user
import arcimoto.db

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

arcimoto.args.register({
    'filter_args': {
        'type': 'dict',
        'nullable': True,
        'default': {}
    }
})


@arcimoto.runtime.handler
@arcimoto.user.require('authorities.vehicle.read')
def list_vehicles(filter_args={}):
    global logger

    # core query and args

    query = (
        'SELECT v.vin, a.authority_keys_id, a.description '
        'FROM vehicle_authority v '
        'LEFT JOIN authority_keys a '
        'ON v.authority_id=a.authority_keys_id ')
    query_args = {}

    # build a where clause out of the filter args using named parameters
    if filter_args:
        filter_vin = filter_args.get('vin', None)
        where = []
        if filter_vin:
            where.append('v.vin ilike %(vin)s')
            query_args['vin'] = '%{}%'.format(filter_vin)

        if len(where) > 0:
            query += 'WHERE '
            query += ' AND '.join(where)

    # handle ordering and ranging
    query += ' ORDER BY v.vin'

    cursor = arcimoto.db.get_cursor()

    # execute the query
    cursor.execute(query, query_args)

    # iterate the results, moving them from cursor tuple to a list of dictionaries for proper jsonification on output
    result = []

    current_vin = None
    vin_record = None
    for record in cursor:

        if record[0] != current_vin:
            vin_record = {
                'vin': record[0],
                'authorities': []
            }
            result.append(vin_record)
            current_vin = record[0]

        vin_record['authorities'].append(record[1])

    return result


lambda_handler = list_vehicles
