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
    },
    'db_cluster_new_identifier': {
        'type': 'string',
        'empty': False,
        'nullable': True,
        'default': None
    }
})


@arcimoto.runtime.handler
def replicate_db_cluster_rename(env, db_cluster_identifier, db_cluster_new_identifier):
    Replicate = replicate.Replicate(env)
    db_cluster_new_name = Replicate.db_cluster_rename(db_cluster_identifier, db_cluster_new_identifier)

    return {
        'db_cluster_identifier': db_cluster_new_name
    }


lambda_handler = replicate_db_cluster_rename
