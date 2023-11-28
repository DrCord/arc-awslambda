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
        'allowed': [
            'dev',
            'staging'
        ],
        'default': None,
        'nullable': True
    },
    'db_cluster_identifier': {
        'type': 'string',
        'empty': False,
        'default': None,
        'nullable': True
    },
    'db_instance_identifier': {
        'type': 'string',
        'empty': False,
        'default': None,
        'nullable': True
    }
})


@arcimoto.runtime.handler
def replicate_db_available(env, db_cluster_identifier, db_instance_identifier):
    Replicate = replicate.Replicate(env)

    db_available = None

    if db_cluster_identifier is None and db_instance_identifier is None:
        raise ArcimotoReplicateAlertException('Either db_cluster_identifier or db_instance_identifier must have a value in the input')

    if db_cluster_identifier is not None:
        db_available = Replicate.db_cluster_status_check(db_cluster_identifier)
    elif db_instance_identifier is not None:
        db_available = Replicate.db_instance_status_check(db_instance_identifier)

    return {
        'db_available': db_available
    }


lambda_handler = replicate_db_available
