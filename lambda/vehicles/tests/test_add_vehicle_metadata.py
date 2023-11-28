import logging
import unittest


from arcimoto.exceptions import *
import arcimoto.runtime
import arcimoto.tests
import vehicles_functions

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class AddVehicleMetadataTestCase(unittest.TestCase):

    @property
    def vin_invalid(self):
        return arcimoto.tests.uuid_vin_get()

    @classmethod
    def setUpClass(cls):
        cls.vin = arcimoto.tests.uuid_vin_get()
        arcimoto.tests.vehicle_create(cls.vin)

    @classmethod
    def tearDownClass(cls):
        arcimoto.tests.vehicle_delete(cls.vin)

    def test_add_vehicle_metadata_success(self):
        self.assertIsInstance(vehicles_functions.add_vehicle_metadata(self.vin, 'unit_test', {'unit-test1': 'test value'}), dict)

    # test errors
    def test_add_vehicle_metadata_error_input_null_vin(self):
        with self.assertRaises(ArcimotoArgumentError):
            vehicles_functions.add_vehicle_metadata(None, 'unit_test', {'unit-test1': 'test value'})

    def test_add_vehicle_metadata_error_input_null_section(self):
        with self.assertRaises(ArcimotoArgumentError):
            vehicles_functions.add_vehicle_metadata(self.vin, None, {'unit-test1': 'test value'})

    def test_add_vehicle_metadata_error_input_null_data(self):
        with self.assertRaises(ArcimotoArgumentError):
            vehicles_functions.add_vehicle_metadata(self.vin, 'unit_test', None)

    def test_add_vehicle_metadata_error_input_invalid_type_vin(self):
        with self.assertRaises(ArcimotoArgumentError):
            vehicles_functions.add_vehicle_metadata(1, 'unit_test', {'unit-test1': 'test value'})

    def test_add_vehicle_metadata_error_input_invalid_type_section(self):
        with self.assertRaises(ArcimotoArgumentError):
            vehicles_functions.add_vehicle_metadata(self.vin, 1, {'unit-test1': 'test value'})

    def test_add_vehicle_metadata_error_input_invalid_type_data(self):
        with self.assertRaises(ArcimotoArgumentError):
            vehicles_functions.add_vehicle_metadata(self.vin, 'unit_test', 'not a dictionary')

    def test_add_vehicle_metadata_error_input_invalid_vin(self):
        with self.assertRaises(ArcimotoNotFoundError):
            vehicles_functions.add_vehicle_metadata(self.vin_invalid, 'unit_test', {'unit-test1': 'test value'})

    def test_add_vehicle_metadata_error_user_unauthorized(self):
        with self.assertRaises(ArcimotoPermissionError):
            vehicles_functions.add_vehicle_metadata(self.vin, 'unit_test', {'unit-test1': 'test value'}, False)


@arcimoto.runtime.handler
def test_add_vehicle_metadata():
    return arcimoto.tests.handle_test_result(unittest.TextTestRunner().run(
        unittest.TestLoader().loadTestsFromTestCase(AddVehicleMetadataTestCase)
    ))


lambda_handler = test_add_vehicle_metadata
