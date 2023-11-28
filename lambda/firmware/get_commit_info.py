import json
import logging

from arcimoto.exceptions import *
import arcimoto.runtime
import arcimoto.user
import arcimoto.db

import firmware as firmware_class

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

arcimoto.args.register({
    'repo': {
        'type': 'string'
    }
})


@arcimoto.runtime.handler
@arcimoto.user.require('firmware.release-version.read')
def get_commit_info(repo):
    '''Get hash of latest master commit of provided repo name in ArcimotoCode'''
    firmware_resources = firmware_class.Firmware()
    return firmware_resources.get_commit_info(firmware_resources.bb_token, repo, 'Comm Firmware.dfu')


lambda_handler = get_commit_info
