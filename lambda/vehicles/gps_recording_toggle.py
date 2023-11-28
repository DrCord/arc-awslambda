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
    },
    'record_gps': {
        'type': 'boolean',
        'required': True
    }
})


@arcimoto.runtime.handler
@arcimoto.user.require('vehicles.vehicle.write')
@arcimoto.db.transaction
def gps_recording_toggle(vin, record_gps):
    global logger

    vehicle_instance = arcimoto.vehicle.Vehicle(vin)
    vehicle_instance.record_gps = record_gps

    return {}


lambda_handler = gps_recording_toggle
