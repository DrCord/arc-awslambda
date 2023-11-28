import logging
import unittest


from arcimoto.exceptions import *
import arcimoto.runtime
import arcimoto.tests
import fleets_functions

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class AddVehicleToGroupTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.test_vin = arcimoto.tests.uuid_vin_get()
        arcimoto.tests.vehicle_create(cls.test_vin)
        cls.vehicle_group_id = fleets_functions.vehicle_group_create()

    @classmethod
    def tearDownClass(cls):
        if cls.vehicle_group_id is not None:
            vehicle_group_vehicles = fleets_functions.vehicle_group_get(cls.vehicle_group_id).get('vehicles', [])
            for vehicle in vehicle_group_vehicles:
                if vehicle == cls.test_vin:
                    fleets_functions.vehicle_group_remove_vehicle(cls.vehicle_group_id, cls.test_vin)
            fleets_functions.vehicle_group_delete(cls.vehicle_group_id)
        arcimoto.tests.vehicle_delete(cls.test_vin)

    def test_add_vehicle_to_group_success(self):
        self.assertIsInstance(fleets_functions.vehicle_group_add_vehicle(self.vehicle_group_id, self.test_vin), dict)

    # test errors
    def test_add_vehicle_to_group_error_input_null_group(self):
        with self.assertRaises(ArcimotoArgumentError):
            fleets_functions.vehicle_group_add_vehicle(None, self.test_vin)

    def test_add_vehicle_to_group_error_input_null_vin(self):
        with self.assertRaises(ArcimotoArgumentError):
            fleets_functions.vehicle_group_add_vehicle(self.vehicle_group_id, None)

    def test_add_vehicle_to_group_error_input_invalid_vehicle_group_id_must_be_positive_integer(self):
        with self.assertRaises(ArcimotoArgumentError):
            fleets_functions.vehicle_group_add_vehicle(-1, self.test_vin)

    def test_add_vehicle_to_group_error_input_invalid_type_vehicle_group_id(self):
        with self.assertRaises(ArcimotoArgumentError):
            fleets_functions.vehicle_group_add_vehicle('not an integer', self.test_vin)

    def test_add_vehicle_to_group_error_input_invalid_type_vin(self):
        with self.assertRaises(ArcimotoArgumentError):
            fleets_functions.vehicle_group_add_vehicle(self.vehicle_group_id, 1)

    def test_add_vehicle_to_group_error_user_unauthorized(self):
        with self.assertRaises(ArcimotoPermissionError):
            fleets_functions.vehicle_group_add_vehicle(self.vehicle_group_id, self.test_vin, False)


@arcimoto.runtime.handler
def test_add_vehicle_to_group():
    return arcimoto.tests.handle_test_result(unittest.TextTestRunner().run(
        unittest.TestLoader().loadTestsFromTestCase(AddVehicleToGroupTestCase)
    ))


lambda_handler = test_add_vehicle_to_group
