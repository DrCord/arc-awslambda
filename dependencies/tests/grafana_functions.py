import logging
import boto3

import arcimoto.runtime
import arcimoto.tests

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


def provision_groups(test_runner_user_admin=True):
    return arcimoto.runtime.test_invoke_lambda('provision_grafana_groups', {}, test_runner_user_admin)


def provision_overview(group_id, test_runner_user_admin=True):
    return arcimoto.runtime.test_invoke_lambda('provision_grafana_overview', {'group_id': group_id}, test_runner_user_admin)


def provision_vehicle(vin, show_gps, test_runner_user_admin=True):
    return arcimoto.runtime.test_invoke_lambda('provision_grafana_vehicle', {'vin': vin, 'show_gps': show_gps}, test_runner_user_admin)
