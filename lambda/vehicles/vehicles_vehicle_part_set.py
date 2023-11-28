import logging

from arcimoto.exceptions import *
import arcimoto.runtime
import arcimoto.args
import arcimoto.user

import parts as parts_class

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

arcimoto.args.register({
    'vin': {
        'type': 'string',
        'required': True
    },
    'part_type': {
        'type': 'string',
        'required': True
    }
})


@arcimoto.runtime.handler
@arcimoto.user.require('vehicles.vehicle.write')
def vehicles_vehicle_part_set(vin, part_type):
    '''
    Installs part on vehicle based on part_type and vehicle model_release
    '''
    parts_resources = parts_class.Parts(None, vin)
    return parts_resources.vehicle_part_install(vin, part_type)


lambda_handler = vehicles_vehicle_part_set
