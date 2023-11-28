import logging

from arcimoto.exceptions import *
import arcimoto.runtime
import arcimoto.args
import arcimoto.user

import parts as parts_class

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

arcimoto.args.register({
    'model_release_id': {
        'type': 'integer',
        'required': True,
        'min': 1
    },
    'part_type': {
        'type': 'string',
        'required': True
    },
    'part_number': {
        'type': 'string',
        'required': True
    }
})


@arcimoto.runtime.handler
@arcimoto.user.require('vehicles.vehicle.write')
def vehicles_model_release_part_set(model_release_id, part_type, part_number):
    parts_resources = parts_class.Parts(model_release_id)
    return parts_resources.model_release_part_set(part_type, part_number)


lambda_handler = vehicles_model_release_part_set
