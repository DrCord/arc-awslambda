import logging

from arcimoto.exceptions import *
import arcimoto.args
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
def replicate_authkey_db_users_restore(env):
    global logger

    ReplicateAuthkey = replicate.ReplicateAuthkey(env, False)
    ReplicateAuthkey.db_instance_users_restore()

    return {}


lambda_handler = replicate_authkey_db_users_restore
