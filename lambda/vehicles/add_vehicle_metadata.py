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
    'section': {
        'type': 'string',
        'required': True
    },
    'data': {
        'type': 'dict',
        'required': True
    },
})


@arcimoto.runtime.handler
@arcimoto.user.require('vehicles.vehicle.write')
@arcimoto.db.transaction
def add_vehicle_metadata(vin, section, data):

    vehicle_instance = arcimoto.vehicle.Vehicle(vin)

    for key, value in data.items():
        vehicle_instance.update_meta(section, key, value)

    return {}


lambda_handler = add_vehicle_metadata
