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
    'model_release_id': {
        'type': 'integer',
        'required': True,
        'min': 1
    }
})


@arcimoto.runtime.handler
@arcimoto.user.require('vehicles.vehicle.write')
def vehicles_vehicle_part_set(vin, model_release_id):
    vehicle_instance = arcimoto.vehicle.Vehicle(vin)
    vehicle_instance.vehicle_model_release_set(model_release_id)
    return {}


lambda_handler = vehicles_vehicle_part_set
