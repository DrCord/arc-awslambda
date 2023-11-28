import logging
import grafana

from arcimoto.exceptions import *
import arcimoto.runtime
import arcimoto.args
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
@arcimoto.user.require('grafana.group.write')
@arcimoto.user.require('grafana.vehicle.write')
@arcimoto.db.transaction
def provision_grafana_overview(group_id):
    group, vehicles = get_vehicles_in_group(group_id)
    grafana_instance = grafana.Grafana()

    try:
        grafana_instance.provision_grafana_group_overview(group, vehicles)
    except Exception as e:
        raise ArcimotoException(f'provision_grafana_overview function failed: {e}')
    else:
        logger.info(f'provision_grafana_overview complete for group {group}')

    try:
        grafana_instance.provision_grafana_group_telemetry(group, vehicles)
    except Exception as e:
        raise ArcimotoException(f'provision_grafana_telemetry function failed: {e}')
    else:
        logger.info(f'provision_grafana_telemetry complete for group {group}')

    return {}


def get_vehicles_in_group(group_id):
    cursor = arcimoto.db.get_cursor()

    # select all vehicles for provided group for overview dashboard creation
    cursor.execute('SELECT id, name FROM vehicle_group WHERE id=%s', (group_id,))
    group = cursor.fetchone()

    if group is None:
        raise ArcimotoNotFoundError('No group found for provided name')

    # get vins for matching group vehicles
    cursor.execute('SELECT vin FROM vehicle_join_vehicle_group WHERE group_id=%s', (group_id, ))
    vins = cursor.fetchall()

    vehicles = []
    if len(vins) != 0:
        # select vehicles for vehicle ids
        cursor.execute('SELECT vin FROM vehicle WHERE vin = ANY(ARRAY[%s])', [vins])
        vehicles = cursor.fetchall()

    return group, vehicles


lambda_handler = provision_grafana_overview
