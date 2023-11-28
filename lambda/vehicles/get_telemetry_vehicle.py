import logging

from arcimoto.exceptions import *
import arcimoto.runtime
import arcimoto.args
import arcimoto.user
import arcimoto.db
import arcimoto.vehicle

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

arcimoto.args.register({
    'vin': {
        'type': 'string',
        'required': True
    }
})


@arcimoto.runtime.handler
def get_telemetry_vehicle(vin):
    current_user = arcimoto.user.current()
    vehicle_instance = arcimoto.vehicle.Vehicle(vin)
    if not vehicle_instance.validate_user_access(current_user.username):
        current_user.assert_permission('vehicles.vehicle.read')

    return vehicle_instance.get()


lambda_handler = get_telemetry_vehicle
