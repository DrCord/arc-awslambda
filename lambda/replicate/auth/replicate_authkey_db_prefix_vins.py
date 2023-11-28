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
def replicate_authkey_db_prefix_vins(env):
    ReplicateAuthkey = replicate.ReplicateAuthkey(env, False)
    ReplicateAuthkey.prefix_vins()

    return {}


lambda_handler = replicate_authkey_db_prefix_vins
