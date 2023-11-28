import logging

from arcimoto.exceptions import *
import arcimoto.runtime
import arcimoto.user
import arcimoto.db

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


@arcimoto.runtime.handler
@arcimoto.user.require('fleets.group.read')
def list_vehicle_groups():
    '''List all vehicle groups (fleets) and corresponding location code and accounting department code from joined tables'''
    global logger

    cursor = arcimoto.db.get_cursor()
    query = (
        'SELECT '
        'vg.id as id, '
        'vg.name as name, '
        'lc.code as location_code, '
        'ac.code as code, '
        'ac.description as description '
        'FROM vehicle_group vg '
        'LEFT JOIN vehicle_group_join_accounting_department_code jc '
        'ON vg.id = jc.vehicle_group_id '
        'LEFT JOIN accounting_department_code ac '
        'ON ac.id = jc.accounting_department_code_id '
        'LEFT JOIN vehicle_group_join_locations AS vg_j_l '
        'ON vg_j_l.group_id = vg.id  '
        'LEFT JOIN location_join_accounting_location_code AS ajc '
        'ON vg_j_l.location_id = ajc.location_id '
        'LEFT JOIN accounting_location_code AS lc '
        'ON lc.id = ajc.accounting_location_code_id '
        'ORDER BY vg.id ASC'
    )
    cursor.execute(query)

    result = []
    for record in cursor:
        result.append(
            {
                'id': record['id'],
                'name': record['name'],
                'location_code': record['location_code'],
                'code': record['code'],
                'description': record['description'],
            }
        )

    return result


lambda_handler = list_vehicle_groups
