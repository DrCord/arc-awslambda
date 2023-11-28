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
@arcimoto.user.require('vehicles.vehicle.provision')
@arcimoto.db.transaction
def unprovision_vehicle_telemetry(vin):
    global logger

    vehicle_instance = arcimoto.vehicle.Vehicle(vin)

    try:
        vehicle_instance.delete()

    except RuntimeError as e:
        logger.exception(f'unprovision_vehicle_telemetry lambda failed with RuntimeError: {e}')
        raise ArcimotoNoStepUnrollException(e)

    return {}


lambda_handler = unprovision_vehicle_telemetry
