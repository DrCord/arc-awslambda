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
    }
})


@arcimoto.runtime.handler
@arcimoto.user.require('vehicles.vehicle.read')
def vehicles_model_release_parts_get(model_release_id):
    parts_resources = parts_class.Parts(model_release_id)
    return parts_resources.model_release_parts


lambda_handler = vehicles_model_release_parts_get
