import logging

from arcimoto.exceptions import *
import arcimoto.runtime
import arcimoto.user
import arcimoto.db

import firmware as firmware_class

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

arcimoto.args.register({
    'firmware_modules_input': {
        'type': 'dict'
    }
})


@arcimoto.runtime.handler
@arcimoto.user.require('firmware.release-version.read')
def firmware_version_get(firmware_modules_input=None):
    firmware_resources = firmware_class.Firmware()
    return firmware_resources.firmware_version_get(firmware_modules_input)


lambda_handler = firmware_version_get
