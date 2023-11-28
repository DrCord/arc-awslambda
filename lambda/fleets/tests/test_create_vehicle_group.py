import logging
import unittest


from arcimoto.exceptions import *
import arcimoto.runtime
import arcimoto.tests
import fleets_functions

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class VehicleGroupCreateTestCase(unittest.TestCase):

    def test_vehicle_group_create_success(self):
        vehicle_group_id = fleets_functions.vehicle_group_create()
        self.assertTrue(vehicle_group_id is not None)
        fleets_functions.vehicle_group_delete(vehicle_group_id)

    # test errors
    def test_vehicle_group_create_error_input_null_group(self):
        with self.assertRaises(ArcimotoArgumentError):
            fleets_functions.vehicle_group_create({'group': None})

    def test_vehicle_group_create_error_input_invalid_type_group(self):
        with self.assertRaises(ArcimotoArgumentError):
            fleets_functions.vehicle_group_create({'group': 1})

    def test_vehicle_group_create_error_input_user_unauthorized(self):
        with self.assertRaises(ArcimotoPermissionError):
            fleets_functions.vehicle_group_create(None, False)


@arcimoto.runtime.handler
def test_vehicle_group_create():
    return arcimoto.tests.handle_test_result(unittest.TextTestRunner().run(
        unittest.TestLoader().loadTestsFromTestCase(VehicleGroupCreateTestCase)
    ))


lambda_handler = test_vehicle_group_create
