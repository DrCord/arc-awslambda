import logging
import unittest

from arcimoto.exceptions import *
import arcimoto.runtime
import arcimoto.tests
import vehicles_functions
import parts as parts_class

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class VehiclesVehiclePartSetTestCase(unittest.TestCase):

    vin = None
    parts = []
    part_type = None
    vehicle_parts = None
    model_release_id = 1

    @property
    def vin_invalid(self):
        return arcimoto.tests.uuid_vin_get()

    @classmethod
    def setUpClass(cls):
        cls.vin = arcimoto.tests.uuid_vin_get()
        arcimoto.tests.vehicle_create(cls.vin, cls.model_release_id)

        cls.parts_resources = parts_class.Parts(cls.model_release_id, cls.vin)
        cls.vehicle_parts = cls.parts_resources.model_release_parts
        if not len(cls.vehicle_parts):
            raise ArcimotoException('No vehicle parts current data available')
        for part_type in cls.vehicle_parts:
            part = {
                'part_type': part_type,
                'part_number': cls.vehicle_parts.get(part_type, None)
            }
            cls.parts.append(part)

        cls.part_type = cls.parts[0].get('part_type')

    @classmethod
    def tearDownClass(cls):
        arcimoto.tests.vehicle_delete(cls.vin)

    def test_vehicles_vehicle_part_set_success(self):
        self.assertIsInstance(vehicles_functions.vehicle_part_install(self.vin, self.part_type), dict)

    # test errors
    def test_vehicles_vehicle_part_set_error_input_null_vin(self):
        with self.assertRaises(ArcimotoArgumentError):
            vehicles_functions.vehicle_part_install(None, self.part_type)

    def test_vehicles_vehicle_part_set_error_null_part_type(self):
        with self.assertRaises(ArcimotoArgumentError):
            vehicles_functions.vehicle_part_install(self.vin, None)

    def test_vehicles_vehicle_part_set_error_input_invalid_vin(self):
        with self.assertRaises(ArcimotoNotFoundError):
            vehicles_functions.vehicle_part_install(self.vin_invalid, self.part_type)

    def test_vehicles_vehicle_part_set_error_invalid_part_type(self):
        with self.assertRaises(ArcimotoNotFoundError):
            vehicles_functions.vehicle_part_install(self.vin, 'Invalid Part Type')

    def test_vehicles_vehicle_part_set_error_input_invalid_type_vin(self):
        with self.assertRaises(ArcimotoArgumentError):
            vehicles_functions.vehicle_part_install(1, self.part_type)

    def test_vehicles_vehicle_part_set_error_invalid_type_part_type(self):
        with self.assertRaises(ArcimotoArgumentError):
            vehicles_functions.vehicle_part_install(self.vin, 1)

    def test_vehicles_vehicle_part_set_error_unauthorized(self):
        with self.assertRaises(ArcimotoPermissionError):
            vehicles_functions.vehicle_part_install(self.vin, self.part_type, False)


@arcimoto.runtime.handler
def test_vehicles_vehicle_part_set():
    return arcimoto.tests.handle_test_result(unittest.TextTestRunner().run(
        unittest.TestLoader().loadTestsFromTestCase(VehiclesVehiclePartSetTestCase)
    ))


lambda_handler = test_vehicles_vehicle_part_set
