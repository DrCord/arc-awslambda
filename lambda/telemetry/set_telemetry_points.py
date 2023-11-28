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
    'telemetry_points': {
        'type': 'dict',
        'required': True,
        'empty': False
    }
})


@arcimoto.runtime.handler
@arcimoto.user.require('telemetry.points.write')
def set_telemetry_points(vin, telemetry_points):
    global logger

    vehicle_instance = arcimoto.vehicle.Vehicle(vin)

    try:
        vehicle_instance.telemetry_points = telemetry_points

    except RuntimeError as e:
        raise ArcimotoNoStepUnrollException(e)

    return {}


lambda_handler = set_telemetry_points
