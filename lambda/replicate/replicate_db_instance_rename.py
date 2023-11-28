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
    },
    'db_instance_new_identifier': {
        'type': 'string',
        'empty': False,
        'nullable': True,
        'default': None
    }
})


@arcimoto.runtime.handler
def replicate_db_instance_rename(env, db_instance_identifier, db_instance_new_identifier):
    Replicate = replicate.Replicate(env)
    db_instance_new_name = Replicate.db_instance_rename(db_instance_identifier, db_instance_new_identifier)

    return {
        'db_instance_identifier': db_instance_new_name
    }


lambda_handler = replicate_db_instance_rename
