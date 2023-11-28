import logging
import unittest


from arcimoto.exceptions import *
import arcimoto.runtime
import arcimoto.tests
import fleets_functions

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class VehicleGroupDeleteTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.vehicle_group_id = fleets_functions.vehicle_group_create()

    def test_vehicle_group_delete_success(self):
        self.assertIsInstance(fleets_functions.vehicle_group_delete(self.vehicle_group_id), dict)

    # test errors
    def test_vehicle_group_delete_error_input_no_group(self):
        with self.assertRaises(ArcimotoArgumentError):
            fleets_functions.vehicle_group_delete(None)

    def test_vehicle_group_delete_error_input_group_id_arcimoto(self):
        with self.assertRaises(ArcimotoArgumentError):
            fleets_functions.vehicle_group_delete(1)

    def test_vehicle_group_delete_error_input_invalid_group_id_must_be_positive_integer_greater_than_1(self):
        with self.assertRaises(ArcimotoArgumentError):
            fleets_functions.vehicle_group_delete(-1)

    def test_vehicle_group_delete_error_input_invalid_type_group_id(self):
        with self.assertRaises(ArcimotoArgumentError):
            fleets_functions.vehicle_group_delete('not an integer')

    def test_vehicle_group_delete_error_user_unauthorized(self):
        with self.assertRaises(ArcimotoPermissionError):
            fleets_functions.vehicle_group_delete(self.vehicle_group_id, False)


@arcimoto.runtime.handler
def test_vehicle_group_delete():
    return arcimoto.tests.handle_test_result(unittest.TextTestRunner().run(
        unittest.TestLoader().loadTestsFromTestCase(VehicleGroupDeleteTestCase)
    ))


lambda_handler = test_vehicle_group_delete
