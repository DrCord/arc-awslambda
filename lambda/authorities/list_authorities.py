import json
import logging

from arcimoto.exceptions import *
import arcimoto.runtime
import arcimoto.args
import arcimoto.user
import arcimoto.db

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

arcimoto.args.register({
    'params': {
        'type': 'dict',
        'nullable': True,
        'default': {}
    }
})


@arcimoto.runtime.handler
@arcimoto.user.require('authorities.authority.read')
@arcimoto.db.transaction
def list_authorities(params={}):
    global logger

    filter_args = {}
    include_vin = False

    if len(params):
        querystring = params.get('querystring', {})
        if querystring:
            filter_args = querystring.get('filter_args', {})
            include_vin = str(querystring.get('include_vin', False)).lower()
            # cast string from params to bool
            if include_vin in ['false', '0', '', 'none']:
                include_vin = False
            else:
                include_vin = True

    # core query
    query = (
        'SELECT authority_keys_id, parent_authority_id, description '
        'FROM authority_keys '
    )

    # build a where clause out of the filter args using named parameters
    where = []
    query_args = {}

    if filter_args:
        if 'id' in filter_args:
            where.append('authority_keys_id=%(id)s')
            query_args['id'] = filter_args['id']
        if 'parent_id' in filter_args:
            where.append('parent_authority_id=%(parent_id)s')
            query_args['parent_id'] = filter_args['parent_id']
        if 'description' in filter_args:
            where.append('description ilike %(description)s')
            query_args['description'] = '%{}%'.format(filter_args['description'])

        if len(where) > 0:
            query += 'WHERE '
            query += ' AND '.join(where)

    # handle ordering and ranging
    query += 'ORDER BY description, authority_keys_id'

    cursor = arcimoto.db.get_cursor()

    # select records with conditions if provided
    cursor.execute(query, query_args)

    result = []
    for record in cursor:
        result.append({
            'id': record[0],
            'parent_id': record[1],
            'description': record[2]
        })

    # deal with include_vin param
    if include_vin:
        query = (
            'SELECT vin '
            'FROM vehicle_authority '
            'WHERE authority_id=%s '
            'ORDER BY vin'
        )
        for vehicle in result:
            cursor.execute(query, [vehicle['id']])
            vehicles = []
            for record in cursor:
                vehicles.append(record[0])

            vehicle['vins'] = vehicles

    return result


lambda_handler = list_authorities
