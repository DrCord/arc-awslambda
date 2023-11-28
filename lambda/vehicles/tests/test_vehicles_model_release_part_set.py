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


class VehiclesModelReleasePartSetTestCase(unittest.TestCase):

    MODEL_RELEASE_ID = 1
    parts = []
    part_type = None
    part_number = None
    vehicle_parts = None

    @classmethod
    def setUpClass(cls):
        cls.parts_resources = parts_class.Parts(cls.MODEL_RELEASE_ID)
        cls.vehicle_parts = cls.parts_resources.model_release_parts
        if not len(cls.vehicle_parts):
            raise ArcimotoException(f'No vehicle parts data available for model release {cls.MODEL_RELEASE_ID}')
        for part_type in cls.vehicle_parts:
            part = {
                'part_type': part_type,
                'part_number': cls.vehicle_parts.get(part_type, None)
            }
            cls.parts.append(part)

        cls.part_type = cls.parts[0].get('part_type')
        cls.part_number = cls.parts[0].get('part_number')

    # no teardown because of setting to data that is same as already existed

    def test_vehicles_model_release_part_set_success(self):
        # since we are using an existing model_release_id we cannot set to another value with db constraints
        self.assertIsInstance(vehicles_functions.part_set(self.MODEL_RELEASE_ID, self.part_type, self.part_number), dict)

    # test errors
    def test_vehicles_model_release_part_set_error_null_model_release_id(self):
        with self.assertRaises(ArcimotoArgumentError):
            vehicles_functions.part_set(None, self.part_type, self.part_number)

    def test_vehicles_model_release_part_set_error_null_part_type(self):
        with self.assertRaises(ArcimotoArgumentError):
            vehicles_functions.part_set(self.MODEL_RELEASE_ID, None, self.part_number)

    def test_vehicles_model_release_part_set_error_null_part_number(self):
        with self.assertRaises(ArcimotoArgumentError):
            vehicles_functions.part_set(self.MODEL_RELEASE_ID, self.part_type, None)

    def test_vehicles_model_release_part_set_error_invalid_model_release_id(self):
        with self.assertRaises(ArcimotoArgumentError):
            vehicles_functions.part_set(0, self.part_type, self.part_number)

    def test_vehicles_model_release_part_set_error_invalid_part_type(self):
        with self.assertRaises(ArcimotoNotFoundError):
            vehicles_functions.part_set(self.MODEL_RELEASE_ID, 'Invalid Part Type', self.part_number)

    def test_vehicles_model_release_part_set_error_invalid_type_model_release_id(self):
        with self.assertRaises(ArcimotoArgumentError):
            vehicles_functions.part_set('not an integer', self.part_type, self.part_number)

    def test_vehicles_model_release_part_set_error_invalid_type_part_type(self):
        with self.assertRaises(ArcimotoArgumentError):
            vehicles_functions.part_set(self.MODEL_RELEASE_ID, 1, self.part_number)

    def test_vehicles_model_release_part_set_error_invalid_type_part_number(self):
        with self.assertRaises(ArcimotoArgumentError):
            vehicles_functions.part_set(self.MODEL_RELEASE_ID, self.part_type, 1)

    def test_vehicles_model_release_part_set_error_unauthorized(self):
        with self.assertRaises(ArcimotoPermissionError):
            vehicles_functions.part_set(self.MODEL_RELEASE_ID, self.part_type, self.part_number, False)


@arcimoto.runtime.handler
def test_vehicles_model_release_part_set():
    return arcimoto.tests.handle_test_result(unittest.TextTestRunner().run(
        unittest.TestLoader().loadTestsFromTestCase(VehiclesModelReleasePartSetTestCase)
    ))


lambda_handler = test_vehicles_model_release_part_set
