import grafana
import logging

from arcimoto.exceptions import *
import arcimoto.runtime
import arcimoto.args
import arcimoto.user
import arcimoto.vehicle

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

arcimoto.args.register({
    'vin': {
        'type': 'string',
        'required': True,
        'empty': False
    },
    'show_gps': {
        'type': 'boolean',
        'nullable': True,
        'default': False
    }
})


@arcimoto.runtime.handler
@arcimoto.user.require('grafana.vehicle.write')
def provision_grafana_vehicle(vin, show_gps):
    vehicle_instance = arcimoto.vehicle.Vehicle(vin)
    grafana_instance = grafana.Grafana()

    try:
        grafana_instance.publish_dashboard(
            vin,
            grafana_instance.vin_folder,
            vehicle_instance.telemetry_points,
            show_gps=show_gps
        )
    except Exception as e:
        raise ArcimotoAlertException(f'provision_grafana_vehicle function failed: {e}')

    return {}


lambda_handler = provision_grafana_vehicle
