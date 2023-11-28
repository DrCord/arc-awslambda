import logging

from arcimoto.exceptions import *
import arcimoto.args
import arcimoto.runtime

import replicate

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

arcimoto.args.register({
    'db_type': {
        'type': 'string',
        'required': True,
        'allowed': [
            'authkey',
            'main'
        ]
    },
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
def replicate_db_cluster_instance_create(db_type, env):
    if db_type == 'authkey':
        Replicate = replicate.ReplicateAuthkey(env)
    elif db_type == 'main':
        Replicate = replicate.ReplicateMain(env)

    return Replicate.db_cluster_instance_create()


lambda_handler = replicate_db_cluster_instance_create
