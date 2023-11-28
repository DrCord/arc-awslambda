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
    'version': {
        'type': 'string',
        'required': True
    }
})


@arcimoto.runtime.handler
@arcimoto.user.require('telemetry.version.write')
def set_telemetry_version(vin, version):

    vehicle_instance = arcimoto.vehicle.Vehicle(vin)

    try:
        vehicle_instance.telemetry_version = version

    except RuntimeError as e:
        raise ArcimotoNoStepUnrollException(e)

    return {}


lambda_handler = set_telemetry_version
