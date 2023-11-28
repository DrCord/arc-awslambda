import logging
import unittest


from arcimoto.exceptions import *
import arcimoto.runtime
import arcimoto.tests
import grafana_functions

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class ProvisionGrafanaGroupsTestCase(unittest.TestCase):

    def test_provision_grafana_groups_success(self):
        self.assertIsInstance(grafana_functions.provision_groups(), dict)

    # test errors
    def test_provision_grafana_groups_error_user_unauthorized(self):
        with self.assertRaises(ArcimotoPermissionError):
            grafana_functions.provision_groups(False)


@arcimoto.runtime.handler
def test_provision_grafana_groups():
    return arcimoto.tests.handle_test_result(unittest.TextTestRunner().run(
        unittest.TestLoader().loadTestsFromTestCase(ProvisionGrafanaGroupsTestCase)
    ))


lambda_handler = test_provision_grafana_groups
