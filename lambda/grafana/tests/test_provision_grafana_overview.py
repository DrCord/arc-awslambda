import logging
import unittest


from arcimoto.exceptions import *
import arcimoto.runtime
import arcimoto.tests
import grafana_functions
import fleets_functions

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class ProvisionGrafanaOverviewTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.vehicle_group_id = fleets_functions.vehicle_group_create()

    @classmethod
    def tearDownClass(cls):
        fleets_functions.vehicle_group_delete(cls.vehicle_group_id)

    def test_provision_grafana_overview_success(self):
        self.assertIsInstance(grafana_functions.provision_overview(self.vehicle_group_id), dict)

    # test errors
    def test_provision_grafana_overview_error_input_null_group_id(self):
        with self.assertRaises(ArcimotoArgumentError):
            grafana_functions.provision_overview(None, False)

    def test_provision_grafana_overview_error_input_invalid_type_group_id(self):
        with self.assertRaises(ArcimotoArgumentError):
            grafana_functions.provision_overview('not an integer', False)

    def test_provision_grafana_overview_error_input_invalid_group_id_must_be_positive_integer(self):
        with self.assertRaises(ArcimotoArgumentError):
            grafana_functions.provision_overview(-1, False)

    def test_provision_grafana_overview_error_user_unauthorized(self):
        with self.assertRaises(ArcimotoPermissionError):
            grafana_functions.provision_overview(self.vehicle_group_id, False)


@arcimoto.runtime.handler
def test_provision_grafana_overview():
    return arcimoto.tests.handle_test_result(unittest.TextTestRunner().run(
        unittest.TestLoader().loadTestsFromTestCase(ProvisionGrafanaOverviewTestCase)
    ))


lambda_handler = test_provision_grafana_overview
