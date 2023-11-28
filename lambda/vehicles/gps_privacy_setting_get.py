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
        'required': True,
        'empty': False
    }
})


@arcimoto.runtime.handler
@arcimoto.user.require('vehicles.vehicle.read')
def gps_privacy_setting_get(vin):

    vehicle_instance = arcimoto.vehicle.Vehicle(vin)

    record_gps = vehicle_instance.record_gps

    return {'record_gps': record_gps}


lambda_handler = gps_privacy_setting_get
