import logging
import boto3

import arcimoto.runtime

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


def ingest_request(args, test_runner_user_admin=True):
    return arcimoto.runtime.test_invoke_lambda('backfill_ingest_request', args, test_runner_user_admin)


def notify_complete(args, test_runner_user_admin=True):
    return arcimoto.runtime.test_invoke_lambda('backfill_notify_complete', args, test_runner_user_admin)


def notify_failed(args, test_runner_user_admin=True):
    return arcimoto.runtime.test_invoke_lambda('backfill_notify_failed', args, test_runner_user_admin)


def s3_delete_file(args, test_runner_user_admin=True):
    return arcimoto.runtime.test_invoke_lambda('backfill_s3_delete_file', args, test_runner_user_admin)


def s3_load_file(args, test_runner_user_admin=True):
    return arcimoto.runtime.test_invoke_lambda('backfill_s3_load_file', args, test_runner_user_admin)


def s3_presigned_url_generate(args, test_runner_user_admin=True):
    return arcimoto.runtime.test_invoke_lambda('backfill_s3_presigned_url_generate', args, test_runner_user_admin)


def state_machine_start(args, test_runner_user_admin=True):
    return arcimoto.runtime.test_invoke_lambda('backfill_state_machine_start', args, test_runner_user_admin)
