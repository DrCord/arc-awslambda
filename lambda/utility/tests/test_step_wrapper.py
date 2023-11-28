import logging
import unittest
import copy

from arcimoto.exceptions import *
import arcimoto.runtime
import arcimoto.tests
import utility_functions

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class StepWrapperTestCase(unittest.TestCase):

    args = {
        'atoms': [
            {
                'lambda': 'gps_privacy_setting_get',
                'output': {
                    'record_gps': 'record_gps'
                }
            },
            {
                'lambda': 'list_telemetry_vehicles',
                'output': {
                    'vehicles': 'vehicles'
                }
            },
            {
                'lambda': 'get_telemetry_vehicle'
            }
        ],
        'input': {
            'vin': None
        }
    }

    @classmethod
    def setUpClass(cls):
        cls.vin = arcimoto.tests.uuid_vin_get()
        arcimoto.tests.vehicle_create(cls.vin)
        cls.args['input']['vin'] = cls.vin

    @classmethod
    def tearDownClass(cls):
        arcimoto.tests.vehicle_delete(cls.vin)

    def test_step_wrapper_success(self):
        args = copy.deepcopy(self.args)
        response = utility_functions.step_wrapper(args)
        self.assertIsInstance(response, dict)
        self.assertIsInstance(response.get('vehicles'), list)
        self.assertFalse(response.get('record_gps'))

    # test errors
    def test_step_wrapper_error_input_null_input(self):
        args = copy.deepcopy(self.args)
        args['input'] = None
        with self.assertRaises(ArcimotoArgumentError):
            utility_functions.step_wrapper(args)

    def test_step_wrapper_error_input_invalid_type_input(self):
        args = copy.deepcopy(self.args)
        args['input'] = 'not a dictionary'
        with self.assertRaises(ArcimotoArgumentError):
            utility_functions.step_wrapper(args)

    def test_step_wrapper_error_input_empty_input(self):
        args = copy.deepcopy(self.args)
        args['input'] = {}
        with self.assertRaises(ArcimotoArgumentError):
            utility_functions.step_wrapper(args)

    def test_step_wrapper_error_input_null_atoms(self):
        args = copy.deepcopy(self.args)
        args['atoms'] = None
        with self.assertRaises(ArcimotoArgumentError):
            utility_functions.step_wrapper(args)

    def test_step_wrapper_error_input_invalid_type_atoms(self):
        args = copy.deepcopy(self.args)
        args['atoms'] = 'not a list'
        with self.assertRaises(ArcimotoArgumentError):
            utility_functions.step_wrapper(args)

    def test_step_wrapper_error_input_empty_atoms(self):
        args = copy.deepcopy(self.args)
        args['atoms'] = []
        with self.assertRaises(ArcimotoArgumentError):
            utility_functions.step_wrapper(args)

    def test_step_wrapper_error_input_atom_missing_lambda_name(self):
        args = copy.deepcopy(self.args)
        del args['atoms'][0]['lambda']
        with self.assertRaises(ArcimotoArgumentError):
            utility_functions.step_wrapper(args)

    def test_step_wrapper_error_user_unauthorized(self):
        args = copy.deepcopy(self.args)
        with self.assertRaises(ArcimotoPermissionError):
            utility_functions.step_wrapper(args, False)


@arcimoto.runtime.handler
def test_step_wrapper():
    return arcimoto.tests.handle_test_result(unittest.TextTestRunner().run(
        unittest.TestLoader().loadTestsFromTestCase(StepWrapperTestCase)
    ))


lambda_handler = test_step_wrapper
