import logging
import unittest
import copy
import uuid

from arcimoto.exceptions import *
import arcimoto.runtime
import arcimoto.tests
import fleets_functions
import vehicles_functions

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class ListTelemetryVehiclesTestCase(unittest.TestCase):

    args = {
        'filter_args': {
            'group_name': None,
            'group_id': None
        }
    }

    @property
    def vehicle_group_id_invalid(self):
        return fleets_functions.vehicle_groups_list()[-1].get('id', 0) + 1

    @classmethod
    def setUpClass(cls):
        cls.vin = arcimoto.tests.uuid_vin_get()
        cls.vin2 = arcimoto.tests.uuid_vin_get()
        cls.vin3 = arcimoto.tests.uuid_vin_get()
        arcimoto.tests.vehicle_create(cls.vin)
        arcimoto.tests.vehicle_create(cls.vin2)
        arcimoto.tests.vehicle_create(cls.vin3)
        cls.vehicles_list = vehicles_functions.list_telemetry_vehicles()
        cls.vehicles_list_len = len(cls.vehicles_list.get('vehicles', []))
        cls.vehicle_group_id = fleets_functions.vehicle_group_create()
        fleets_functions.vehicle_group_add_vehicle(cls.vehicle_group_id, cls.vin)
        fleets_functions.vehicle_group_add_vehicle(cls.vehicle_group_id, cls.vin2)

    @classmethod
    def tearDownClass(cls):
        fleets_functions.vehicle_group_delete(cls.vehicle_group_id)
        arcimoto.tests.vehicle_delete(cls.vin3)
        arcimoto.tests.vehicle_delete(cls.vin2)
        arcimoto.tests.vehicle_delete(cls.vin)

    def test_list_telemetry_vehicles_success_input_null(self):
        self.assertIsInstance(vehicles_functions.list_telemetry_vehicles(), dict)
        self.assertTrue(2 < self.vehicles_list_len)

    def test_list_telemetry_vehicles_success_input_filter_args_group_name(self):
        args = copy.deepcopy(self.args)
        args['filter_args']['group_name'] = 'Unit Test'
        vehicles_list_filtered = vehicles_functions.list_telemetry_vehicles(args)
        self.assertIsInstance(vehicles_list_filtered, dict)
        vehicles_list_filtered_len = len(vehicles_list_filtered.get('vehicles', []))
        self.assertTrue(vehicles_list_filtered_len < self.vehicles_list_len)

    def test_list_telemetry_vehicles_success_input_filter_args_group_id(self):
        args = copy.deepcopy(self.args)
        args['filter_args']['group_id'] = self.vehicle_group_id
        vehicles_list_filtered = vehicles_functions.list_telemetry_vehicles(args)
        self.assertIsInstance(vehicles_list_filtered, dict)
        vehicles_list_filtered_len = len(vehicles_list_filtered.get('vehicles', []))
        self.assertTrue(vehicles_list_filtered_len < self.vehicles_list_len)

    # test errors
    def test_list_telemetry_vehicles_error_input_invalid_type_filter_args(self):
        args = copy.deepcopy(self.args)
        args['filter_args'] = 'not a dictionary'
        with self.assertRaises(ArcimotoArgumentError):
            vehicles_functions.list_telemetry_vehicles(args)

    def test_list_telemetry_vehicles_error_input_invalid_filter_args_group_id(self):
        args = copy.deepcopy(self.args)
        args['filter_args']['group_id'] = self.vehicle_group_id_invalid
        with self.assertRaises(ArcimotoNotFoundError):
            vehicles_functions.list_telemetry_vehicles(args)

    def test_list_telemetry_vehicles_error_input_invalid_filter_args_group_name(self):
        args = copy.deepcopy(self.args)
        args['filter_args']['group_name'] = 'Invalid Group Name' + '-' + uuid.uuid4().hex
        with self.assertRaises(ArcimotoNotFoundError):
            vehicles_functions.list_telemetry_vehicles(args)

    def test_list_telemetry_vehicles_error_user_unauthorized(self):
        with self.assertRaises(ArcimotoPermissionError):
            vehicles_functions.list_telemetry_vehicles({}, False)


@arcimoto.runtime.handler
def test_list_telemetry_vehicles():
    return arcimoto.tests.handle_test_result(unittest.TextTestRunner().run(
        unittest.TestLoader().loadTestsFromTestCase(ListTelemetryVehiclesTestCase)
    ))


lambda_handler = test_list_telemetry_vehicles
