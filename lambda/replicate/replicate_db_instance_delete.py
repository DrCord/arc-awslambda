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
    'db_instance_identifier': {
        'type': 'string',
        'required': True,
        'empty': False
    }
})


@arcimoto.runtime.handler
def replicate_db_instance_delete(env, db_instance_identifier):
    Replicate = replicate.Replicate(env)
    Replicate.db_instance_delete(db_instance_identifier)

    return {}


lambda_handler = replicate_db_instance_delete
