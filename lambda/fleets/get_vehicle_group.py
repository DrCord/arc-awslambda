import logging

from arcimoto.exceptions import *
import arcimoto.runtime
import arcimoto.user
import arcimoto.db

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

arcimoto.args.register({
    'group_id': {
        'type': 'integer',
        'required': True,
        'min': 1
    }
})


@arcimoto.runtime.handler
@arcimoto.user.require('fleets.group.read')
def get_vehicle_group(group_id):
    '''Get vehicle group (fleet) by id. Returns all fleet data as well as joined data, where possible.'''
    global logger

    cursor = arcimoto.db.get_cursor()

    output = {}
    query = (
        'SELECT '
        'vg.name as name, '
        'ac.code as code, '
        'ac.description as description '
        'FROM vehicle_group vg '
        'LEFT JOIN vehicle_group_join_accounting_department_code jc '
        'ON vg.id = jc.vehicle_group_id '
        'LEFT JOIN accounting_department_code ac '
        'ON ac.id = jc.accounting_department_code_id '
        'WHERE vg.id=%s'
    )
    cursor.execute(query, [group_id])
    if cursor.rowcount != 1:
        raise ArcimotoArgumentError('Invalid group_id')
    row = cursor.fetchone()
    output['name'] = row['name']
    output['code'] = row['code']
    output['description'] = row['description']
    output['vehicles'] = []
    output['users'] = []
    output['type'] = None
    output['location'] = None

    query = (
        'SELECT v.vin '
        'FROM vehicle v '
        'LEFT JOIN vehicle_join_vehicle_group vj '
        'ON v.vin=vj.vin '
        'WHERE vj.group_id=%s'
    )
    cursor.execute(query, [group_id])
    for row in cursor:
        output['vehicles'].append(row['vin'])

    query = (
        'SELECT username '
        'FROM users_join_vehicle_group '
        'WHERE vehicle_group=%s'
    )
    cursor.execute(query, [group_id])
    for row in cursor:
        output['users'].append(row['username'])

    # get type
    query = (
        'SELECT vgt.group_type '
        'FROM vehicle_group_join_vehicle_group_type AS vg_j_vgt '
        'JOIN vehicle_group_type AS vgt ON vgt.id = vg_j_vgt.type_id '
        'WHERE vg_j_vgt.group_id=%s'
    )
    cursor.execute(query, [group_id])
    if cursor.rowcount == 1:
        row = cursor.fetchone()
        output['type'] = row['group_type']

    # get location
    query = (
        'SELECT vg_j_l.location_id, '
        'l.location_name, '
        'lc.code as location_code, '
        'l.street_number, '
        'l.structure_name, '
        'l.street_number_suffix, '
        'l.street_name, '
        'l.street_type, '
        'l.street_direction, '
        'lat.address_type, '
        'l.address_type_identifier, '
        'l.city, '
        'l.governing_district, '
        'l.postal_area, '
        'l.local_municipality, '
        'l.country, '
        'l.gps_latitude, '
        'l.gps_longitude '
        'FROM vehicle_group_join_locations AS vg_j_l '
        'JOIN locations AS l on l.id = vg_j_l.location_id '
        'LEFT JOIN locations_address_types AS lat '
        'ON l.address_type = lat.id '
        'LEFT JOIN location_join_accounting_location_code AS jc '
        'ON l.id = jc.location_id '
        'LEFT JOIN accounting_location_code AS lc '
        'ON lc.id = jc.accounting_location_code_id '
        'WHERE vg_j_l.group_id=%s'
    )
    cursor.execute(query, [group_id])
    if cursor.rowcount == 1:
        row = cursor.fetchone()
        output['location'] = {
            'id': row['location_id'],
            'location_name': row['location_name'],
            'location_code': row['location_code'],
            'street_number': row['street_number'],
            'structure_name': row['structure_name'],
            'street_number_suffix': row['street_number_suffix'],
            'street_name': row['street_name'],
            'street_type': row['street_type'],
            'street_direction': row['street_direction'],
            'address_type': row['address_type'],
            'address_type_identifier': row['address_type_identifier'],
            'city': row['city'],
            'governing_district': row['governing_district'],
            'postal_area': row['postal_area'],
            'local_municipality': row['local_municipality'],
            'country': row['country'],
            'gps_latitude': row['gps_latitude'],
            'gps_longitude': row['gps_longitude']
        }

    return output


lambda_handler = get_vehicle_group
