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
        'required': True
    },
    'thingID': {
        'rename': 'vin'
    }
})


@arcimoto.runtime.handler
@arcimoto.user.require('telemetry.points.read')
@arcimoto.db.transaction
def get_telemetry_points(vin):
    global logger

    vehicle_instance = arcimoto.vehicle.Vehicle(vin)

    try:
        telemetry_points = vehicle_instance.telemetry_points

    except RuntimeError as e:
        raise ArcimotoNoStepUnrollException(e)

    return telemetry_points


lambda_handler = get_telemetry_points
