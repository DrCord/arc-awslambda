import logging
import unittest


from arcimoto.exceptions import *
import arcimoto.runtime
import arcimoto.tests
import fleets_functions

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class VehicleGroupGetTestCase(unittest.TestCase):

    @property
    def group_id_invalid(self):
        return self.vehicle_groups[-1].get('id', 0) + 1

    @classmethod
    def setUpClass(cls):
        cls.vehicle_group_id = fleets_functions.vehicle_group_create()
        cls.vehicle_groups = fleets_functions.vehicle_groups_list()

    @classmethod
    def tearDownClass(cls):
        if cls.vehicle_group_id is not None:
            fleets_functions.vehicle_group_delete(cls.vehicle_group_id)

    def test_vehicle_group_get_success(self):
        response = fleets_functions.vehicle_group_get(self.vehicle_group_id)
        self.assertIsInstance(response, dict)

    # test errors
    def test_vehicle_group_get_error_input_null_group_id(self):
        with self.assertRaises(ArcimotoArgumentError):
            fleets_functions.vehicle_group_get(None)

    def test_vehicle_group_get_error_input_group_id_must_be_positive_integer(self):
        with self.assertRaises(ArcimotoArgumentError):
            fleets_functions.vehicle_group_get(-1)

    def test_vehicle_group_get_error_invalid_group_id(self):
        with self.assertRaises(ArcimotoArgumentError):
            fleets_functions.vehicle_group_get(self.group_id_invalid)

    def test_vehicle_group_get_error_invalid_type_group_id(self):
        with self.assertRaises(ArcimotoArgumentError):
            fleets_functions.vehicle_group_get('not an integer')

    def test_vehicle_group_get_error_user_unauthorized(self):
        with self.assertRaises(ArcimotoPermissionError):
            fleets_functions.vehicle_group_get(self.vehicle_group_id, False)


@arcimoto.runtime.handler
def test_vehicle_group_get():
    return arcimoto.tests.handle_test_result(unittest.TextTestRunner().run(
        unittest.TestLoader().loadTestsFromTestCase(VehicleGroupGetTestCase)
    ))


lambda_handler = test_vehicle_group_get
