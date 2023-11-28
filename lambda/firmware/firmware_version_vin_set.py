import logging

from arcimoto.exceptions import *
import arcimoto.runtime
import arcimoto.user
import arcimoto.db
import arcimoto.vehicle

import firmware as firmware_class

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

arcimoto.args.register({
    'vin': {
        'type': 'string',
        'required': True
    },
    'firmware_modules': {
        'type': 'dict',
        'required': True
    }
})


@arcimoto.runtime.handler
@arcimoto.user.require('firmware.vehicle.write')
# comment to force update
def firmware_version_vin_set(vin, firmware_modules):
    firmware_resources = firmware_class.Firmware()
    return firmware_resources.firmware_version_vin_set(vin, firmware_modules)


lambda_handler = firmware_version_vin_set
