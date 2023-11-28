import logging
import boto3

from arcimoto.exceptions import *
import arcimoto.runtime

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


def verify_dl(args, test_runner_user_admin=True):
    return arcimoto.runtime.test_invoke_lambda('sheer_id_verify_dl', args, test_runner_user_admin)
