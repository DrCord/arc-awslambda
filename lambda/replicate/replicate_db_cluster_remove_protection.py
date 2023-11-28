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
    },
    'db_cluster_identifier': {
        'type': 'string',
        'required': True,
        'empty': False
    }
})


@arcimoto.runtime.handler
def replicate_db_cluster_remove_protection(env, db_cluster_identifier):
    Replicate = replicate.Replicate(env)
    Replicate.db_cluster_remove_protection(db_cluster_identifier)

    return {}


lambda_handler = replicate_db_cluster_remove_protection
