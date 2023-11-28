import logging
import unittest
import copy

from arcimoto.exceptions import *
import arcimoto.runtime
import arcimoto.tests
import fleets_functions

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class VehicleGroupTypeSetTestCase(unittest.TestCase):

    vehicle_group_id = None
    args = {
        'vehicle_group_id': None,
        'type_id': 1
    }

    @property
    def group_id_invalid(self):
        return fleets_functions.vehicle_groups_list()[-1].get('id', 0) + 1

    @classmethod
    def setUpClass(cls):
        # vehicle group
        cls.vehicle_group_id = fleets_functions.vehicle_group_create()        
        if cls.vehicle_group_id is None:
            raise ArcimotoException('Unable to create vehicle group for unit tests setup')
        cls.args['vehicle_group_id'] = cls.vehicle_group_id

    @classmethod
    def tearDownClass(cls):
        if cls.vehicle_group_id is not None:
            fleets_functions.vehicle_group_delete(cls.vehicle_group_id)

    def test_vehicle_group_type_set_success(self):
        self.assertIsInstance(fleets_functions.vehicle_group_type_set(self.args), dict)

    # test errors
    def test_vehicle_group_type_set_error_input_null_vehicle_group_id(self):
        args = copy.deepcopy(self.args)
        args['vehicle_group_id'] = None
        with self.assertRaises(ArcimotoArgumentError):
            fleets_functions.vehicle_group_type_set(args)

    def test_vehicle_group_type_set_error_input_invalid_type_vehicle_group_id(self):
        args = copy.deepcopy(self.args)
        args['vehicle_group_id'] = 'not an integer'
        with self.assertRaises(ArcimotoArgumentError):
            fleets_functions.vehicle_group_type_set(args)

    def test_vehicle_group_type_set_error_input_invalid_type_type_id(self):
        args = copy.deepcopy(self.args)
        args['type_id'] = 'not an integer'
        with self.assertRaises(ArcimotoArgumentError):
            fleets_functions.vehicle_group_type_set(args)

    def test_vehicle_group_type_set_error_input_invalid_vehicle_group_id_must_be_positive_integer(self):
        args = copy.deepcopy(self.args)
        args['vehicle_group_id'] = -1
        with self.assertRaises(ArcimotoArgumentError):
            fleets_functions.vehicle_group_type_set(args)

    def test_vehicle_group_type_set_error_invalid_vehicle_group_id(self):
        args = copy.deepcopy(self.args)
        args['vehicle_group_id'] = self.group_id_invalid
        with self.assertRaises(ArcimotoNotFoundError):
            fleets_functions.vehicle_group_type_set(args)

    def test_vehicle_group_type_set_error_user_unauthorized(self):
        with self.assertRaises(ArcimotoPermissionError):
            fleets_functions.vehicle_group_type_set(self.args, False)


@arcimoto.runtime.handler
def test_vehicle_group_type_set():
    return arcimoto.tests.handle_test_result(unittest.TextTestRunner().run(
        unittest.TestLoader().loadTestsFromTestCase(VehicleGroupTypeSetTestCase)
    ))


lambda_handler = test_vehicle_group_type_set
