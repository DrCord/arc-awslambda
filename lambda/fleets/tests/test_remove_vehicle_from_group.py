import logging
import unittest


from arcimoto.exceptions import *
import arcimoto.runtime
import arcimoto.tests
import fleets_functions

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class RemoveVehicleFromGroupTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.vin = arcimoto.tests.test_vin_get()
        arcimoto.tests.vehicle_create(cls.vin)
        cls.vehicle_group_id = fleets_functions.vehicle_group_create()
        fleets_functions.vehicle_group_add_vehicle(cls.vehicle_group_id, cls.vin)

    @classmethod
    def tearDownClass(cls):
        if cls.vehicle_group_id is not None:
            fleets_functions.vehicle_group_delete(cls.vehicle_group_id)
        arcimoto.tests.vehicle_delete()

    def test_remove_vehicle_from_group_success(self):
        self.assertIsInstance(fleets_functions.vehicle_group_remove_vehicle(self.vehicle_group_id, self.vin), dict)

    # test errors
    def test_remove_vehicle_from_group_error_input_null_group(self):
        with self.assertRaises(ArcimotoArgumentError):
            fleets_functions.vehicle_group_remove_vehicle(None, self.vin)

    def test_remove_vehicle_from_group_error_input_null_vin(self):
        with self.assertRaises(ArcimotoArgumentError):
            fleets_functions.vehicle_group_remove_vehicle(self.vehicle_group_id, None)

    def test_remove_vehicle_from_group_error_input_invalid_type_group_id(self):
        with self.assertRaises(ArcimotoArgumentError):
            fleets_functions.vehicle_group_remove_vehicle('not an integer', self.vin)

    def test_remove_vehicle_from_group_error_input_invalid_group_id_must_be_positive_integer(self):
        with self.assertRaises(ArcimotoArgumentError):
            fleets_functions.vehicle_group_remove_vehicle(-1, self.vin)

    def test_remove_vehicle_from_group_error_input_invalid_type_vin(self):
        with self.assertRaises(ArcimotoArgumentError):
            fleets_functions.vehicle_group_remove_vehicle(self.vehicle_group_id, 1)

    def test_remove_vehicle_from_group_error_user_unauthorized(self):
        with self.assertRaises(ArcimotoPermissionError):
            fleets_functions.vehicle_group_remove_vehicle(self.vehicle_group_id, self.vin, False)


@arcimoto.runtime.handler
def test_remove_vehicle_from_group():
    return arcimoto.tests.handle_test_result(unittest.TextTestRunner().run(
        unittest.TestLoader().loadTestsFromTestCase(RemoveVehicleFromGroupTestCase)
    ))


lambda_handler = test_remove_vehicle_from_group
