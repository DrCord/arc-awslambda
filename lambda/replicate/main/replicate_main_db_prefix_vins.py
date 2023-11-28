import logging

from arcimoto.exceptions import *
import arcimoto.args
import arcimoto.db
import arcimoto.runtime

import replicate

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

arcimoto.args.register({
    'env': {
        'type': 'string',
        'required': True,
        'allowed': [
            'dev',
            'staging'
        ]
    }
})


@arcimoto.runtime.handler
@arcimoto.db.transaction
def replicate_main_db_prefix_vins(env):
    ReplicateMain = replicate.ReplicateMain(env, False)
    ReplicateMain.prefix_vins()

    return {}


lambda_handler = replicate_main_db_prefix_vins
