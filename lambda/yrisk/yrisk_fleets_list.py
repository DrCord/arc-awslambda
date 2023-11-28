import logging

from arcimoto.exceptions import *
import arcimoto.runtime
import arcimoto.db

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


@arcimoto.runtime.handler
def yrisk_fleets_list():
    global logger

    cursor = arcimoto.db.get_cursor()

    query = (
        'SELECT vg.id '
        'FROM vehicle_group AS vg '
        'JOIN vehicle_group_join_locations as vg_j_l ON vg.id = vg_j_l.group_id '
        'JOIN vehicle_group_join_vehicle_group_type as vg_j_vgt ON vg.id = vg_j_vgt.group_id '
        'WHERE vg_j_l.location_id IS NOT NULL '
        'AND vg_j_vgt.type_id IS NOT NULL'
    )
    vehicle_groups = []
    cursor.execute(query, [])
    for record in cursor:
        vehicle_groups.append(record['id'])

    return {
        'vehicle_groups': sorted(vehicle_groups)
    }


lambda_handler = yrisk_fleets_list
