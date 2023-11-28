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
        'empty': False,
        'nullable': True,
        'default': None
    },
    'db_instance_identifier': {
        'type': 'string',
        'empty': False,
        'nullable': True,
        'default': None
    }
})


@arcimoto.runtime.handler
def replicate_db_exists(env, db_cluster_identifier, db_instance_identifier):
    Replicate = replicate.Replicate(env)

    db_exists = None

    if db_cluster_identifier is None and db_instance_identifier is None:
        raise ArcimotoReplicateAlertException('Either db_cluster_identifier or db_instance_identifier must have a value in the input')

    if db_cluster_identifier is not None:
        db_exists = Replicate.db_cluster_exists(db_cluster_identifier)
    elif db_instance_identifier is not None:
        db_exists = Replicate.db_instance_exists(db_instance_identifier)

    return {
        'db_exists': db_exists
    }


lambda_handler = replicate_db_exists
