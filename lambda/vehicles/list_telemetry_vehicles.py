import logging

from arcimoto.exceptions import *
import arcimoto.runtime
import arcimoto.args
import arcimoto.user
import arcimoto.db

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

arcimoto.args.register({
    'filter_args': {
        'type': 'dict'
    }
})


@arcimoto.runtime.handler
@arcimoto.user.require('vehicles.vehicle.read')
def list_telemetry_vehicles(filter_args={}):
    global logger

    cursor = arcimoto.db.get_cursor()

    vehicle_query = (
        'SELECT vin '
        'FROM vehicle '
    )
    vehicles = []

    if filter_args:
        filter_group_name = filter_args.get('group_name', None)
        filter_group_id = filter_args.get('group_id', None)

        if filter_group_id or filter_group_name:
            groups = []
            filter_query = (
                'SELECT id '
                'FROM vehicle_group '
                'WHERE '
            )
            if filter_group_id:
                filter_query += 'id=%s'
                params = [filter_group_id]
            else:
                filter_query += 'name=%s'
                params = [filter_group_name]
            cursor.execute(filter_query, params)
            for record in cursor:
                groups.append(record[0])
            if len(groups) == 0:
                if filter_group_id:
                    raise ArcimotoNotFoundError(f'Group id {filter_group_id} not found')
                else:
                    raise ArcimotoNotFoundError(f'Group name {filter_group_name} not found')
            filter_group_vins_query = (
                'SELECT vin '
                'FROM vehicle_join_vehicle_group '
                'WHERE group_id in %s'
            )
            cursor.execute(filter_group_vins_query, [tuple(groups)])
            vins = []
            for record in cursor:
                vins.append(record[0])
            if (len(vins) > 0):
                vehicle_query += (
                    'WHERE vin in %s '
                    'ORDER BY vin'
                )
                cursor.execute(vehicle_query, (tuple(vins), ))
                for record in cursor:
                    vehicles.append(
                        {
                            'vin': record[0]
                        }
                    )
    else:
        vehicle_query += 'ORDER BY vin'
        cursor.execute(vehicle_query)
        for record in cursor:
            vehicles.append(
                {
                    'vin': record[0]
                }
            )

    return {
        'vehicles': vehicles
    }


lambda_handler = list_telemetry_vehicles
