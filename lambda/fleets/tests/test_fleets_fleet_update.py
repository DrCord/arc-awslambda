import logging
import unittest
from copy import deepcopy

from arcimoto.exceptions import *
import arcimoto.runtime
import arcimoto.tests
import fleets_functions

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class FleetsFleetUpdateTestCase(unittest.TestCase):

    args = {
        'fleet_name': 'Unit Test',
        'id': None
    }
    vehicle_group_id = None

    @classmethod
    def setUpClass(cls):
        cls.vehicle_group_id = fleets_functions.vehicle_group_create()
        cls.args['id'] = cls.vehicle_group_id

    @classmethod
    def tearDownClass(cls):
        fleets_functions.vehicle_group_delete(cls.vehicle_group_id)

    def test_fleets_fleet_update_success(self):
        self.assertIsInstance(fleets_functions.fleet_update(self.args), dict)

    # test errors
    def test_fleets_fleet_update_error_input_null_id(self):
        args = deepcopy(self.args)
        args['id'] = None
        with self.assertRaises(ArcimotoArgumentError):
            fleets_functions.fleet_update(args)

    def test_fleets_fleet_update_error_input_min_id(self):
        args = deepcopy(self.args)
        args['id'] = -1
        with self.assertRaises(ArcimotoArgumentError):
            fleets_functions.fleet_update(args)

    def test_fleets_fleet_update_error_input_invalid_type_id(self):
        args = deepcopy(self.args)
        args['id'] = 'not an integer'
        with self.assertRaises(ArcimotoArgumentError):
            fleets_functions.fleet_update(args)

    def test_fleets_fleet_update_error_input_null_fleet_name(self):
        args = deepcopy(self.args)
        args['fleet_name'] = None
        with self.assertRaises(ArcimotoArgumentError):
            fleets_functions.fleet_update(args)

    def test_fleets_fleet_update_error_input_empty_fleet_name(self):
        args = deepcopy(self.args)
        args['fleet_name'] = ''
        with self.assertRaises(ArcimotoArgumentError):
            fleets_functions.fleet_update(args)

    def test_fleets_fleet_update_error_input_invalid_type_fleet_name(self):
        args = deepcopy(self.args)
        args['fleet_name'] = 1
        with self.assertRaises(ArcimotoArgumentError):
            fleets_functions.fleet_update(args)

    def test_fleets_fleet_update_error_input_user_unauthorized(self):
        with self.assertRaises(ArcimotoPermissionError):
            fleets_functions.fleet_update(self.args, False)


@arcimoto.runtime.handler
def test_fleets_fleet_update():
    return arcimoto.tests.handle_test_result(unittest.TextTestRunner().run(
        unittest.TestLoader().loadTestsFromTestCase(FleetsFleetUpdateTestCase)
    ))


lambda_handler = test_fleets_fleet_update
