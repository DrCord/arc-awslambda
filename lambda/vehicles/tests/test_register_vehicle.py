import logging
import unittest


from arcimoto.exceptions import *
import arcimoto.runtime
import arcimoto.tests
import vehicles_functions

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class RegisterVehicleTestCase(unittest.TestCase):

    MODEL_RELEASE_ID_PRE_DISCOBOARD = 1
    MODEL_RELEASE_ID_DISCOBOARD = 2

    data_pre_discoboard = {
        'message': 'Created by unit test',
        'iccid': '867-5309',
        'board': 1043,  # pre-disco board
        'telemetry_settings:version': 'AsjutNU2.QbEvkFL0K9PHM6ssR4VLjwu',
        'color': 'invisible',
        'owner': 'Software Engineering'
    }
    data_discoboard = {
        'message': 'Created by unit test',
        'iccid': '867-5309',
        'board': 1105,  # disco board
        'telemetry_settings:version': 'AsjutNU2.QbEvkFL0K9PHM6ssR4VLjwu',
        'color': 'invisible',
        'owner': 'Software Engineering'
    }

    @classmethod
    def setUpClass(cls):
        cls.vin1 = arcimoto.tests.uuid_vin_get()
        cls.vin2 = arcimoto.tests.uuid_vin_get()
        arcimoto.tests.vehicle_create(cls.vin1, cls.MODEL_RELEASE_ID_PRE_DISCOBOARD)
        arcimoto.tests.vehicle_create(cls.vin2, cls.MODEL_RELEASE_ID_DISCOBOARD)

    @classmethod
    def tearDownClass(cls):
        arcimoto.tests.vehicle_delete(cls.vin1)
        arcimoto.tests.vehicle_delete(cls.vin2)

    def test_register_vehicle_success_pre_discoboard(self):
        self.assertIsInstance(vehicles_functions.register_vehicle(self.vin1, self.data_pre_discoboard), dict)

    def test_register_vehicle_success_discoboard(self):
        self.assertIsInstance(vehicles_functions.register_vehicle(self.vin2, self.data_discoboard), dict)

    # test errors
    def test_register_vehicle_error_input_null_vin(self):
        with self.assertRaises(Exception):
            vehicles_functions.register_vehicle(None, self.data_discoboard)

    def test_register_vehicle_error_input_null_data(self):
        with self.assertRaises(Exception):
            vehicles_functions.register_vehicle(self.vin1, None)

    # Discoboard mismatch: registration and model release do not match
    def test_register_vehicle_error_discoboard_mismatch(self):
        with self.assertRaises(Exception):
            vehicles_functions.register_vehicle(self.vin1, self.data_discoboard)
        with self.assertRaises(Exception):
            vehicles_functions.register_vehicle(self.vin2, self.data_pre_discoboard)


@arcimoto.runtime.handler
def test_register_vehicle():
    return arcimoto.tests.handle_test_result(unittest.TextTestRunner().run(
        unittest.TestLoader().loadTestsFromTestCase(RegisterVehicleTestCase)
    ))


lambda_handler = test_register_vehicle
