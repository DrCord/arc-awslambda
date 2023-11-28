import logging
import unittest
import uuid

from arcimoto.exceptions import *
import arcimoto.runtime
import arcimoto.tests
import fleets_functions

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class FleetsStatisticsGetTestCase(unittest.TestCase):

    fleet_name = 'Fleet Statistics Get Unit Test'
    vehicle_group_id = None
    vehicle_groups = None

    @property
    def group_id_invalid(self):
        return self.vehicle_groups[-1].get('id', 0) + 1

    @classmethod
    def setUpClass(cls):
        cls.vehicle_group_id = fleets_functions.vehicle_group_create({'group': cls.fleet_name})
        cls.vehicle_groups = fleets_functions.vehicle_groups_list()

    @classmethod
    def tearDownClass(cls):
        if cls.vehicle_group_id is not None:
            fleets_functions.vehicle_group_delete(cls.vehicle_group_id)

    def test_fleets_statistics_get_success(self):
        response = fleets_functions.statistics_get(self.fleet_name)
        self.assertIsInstance(response, dict)

    # test errors
    def test_fleets_statistics_get_error_input_null_fleet_name(self):
        with self.assertRaises(ArcimotoArgumentError):
            fleets_functions.statistics_get(None)

    def test_fleets_statistics_get_error_invalid_fleet_name(self):
        invalid_fleet_name = f'{self.fleet_name}-{uuid.uuid4().hex}'
        with self.assertRaises(ArcimotoArgumentError):
            fleets_functions.statistics_get(invalid_fleet_name)

    def test_fleets_statistics_get_error_invalid_type_fleet_name(self):
        with self.assertRaises(ArcimotoArgumentError):
            fleets_functions.statistics_get(1)


@arcimoto.runtime.handler
def test_fleets_statistics_get():
    return arcimoto.tests.handle_test_result(unittest.TextTestRunner().run(
        unittest.TestLoader().loadTestsFromTestCase(FleetsStatisticsGetTestCase)
    ))


lambda_handler = test_fleets_statistics_get
