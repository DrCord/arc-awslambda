import logging
import unittest


from arcimoto.exceptions import *
import arcimoto.runtime
import arcimoto.tests
import fleets_functions

ARCIMOTO_GROUP_ID = 1

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class RemoveVehicleFromArcimotoGroupTestCase(unittest.TestCase):

    vin = arcimoto.tests.uuid_vin_get()

    @classmethod
    def setUpClass(cls):
        arcimoto.tests.vehicle_create(cls.vin)
        fleets_functions.vehicle_group_add_vehicle(ARCIMOTO_GROUP_ID, cls.vin)

    @classmethod
    def tearDownClass(cls):
        arcimoto.tests.vehicle_delete(cls.vin)

    def test_remove_vehicle_from_arcimoto_group_success(self):
        self.assertIsInstance(fleets_functions.vehicle_group_arcimoto_remove_vehicle(self.vin), dict)

    # test errors
    def test_remove_vehicle_from_arcimoto_group_error_input_null_vin(self):
        with self.assertRaises(ArcimotoArgumentError):
            fleets_functions.vehicle_group_arcimoto_remove_vehicle(None)

    def test_remove_vehicle_from_arcimoto_group_error_input_invalid_type_vin(self):
        with self.assertRaises(ArcimotoArgumentError):
            fleets_functions.vehicle_group_arcimoto_remove_vehicle(1)

    def test_remove_vehicle_from_arcimoto_group_error_user_unauthorized(self):
        with self.assertRaises(ArcimotoPermissionError):
            fleets_functions.vehicle_group_arcimoto_remove_vehicle(self.vin, False)


@arcimoto.runtime.handler
def test_remove_vehicle_from_arcimoto_group():
    return arcimoto.tests.handle_test_result(unittest.TextTestRunner().run(
        unittest.TestLoader().loadTestsFromTestCase(RemoveVehicleFromArcimotoGroupTestCase)
    ))


lambda_handler = test_remove_vehicle_from_arcimoto_group
