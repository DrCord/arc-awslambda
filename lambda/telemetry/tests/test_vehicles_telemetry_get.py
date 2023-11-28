import logging
import unittest

from arcimoto.exceptions import *
import arcimoto.runtime
import arcimoto.tests
import fleets_functions
import telemetry_functions

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class VehiclesTelemetryGetTestCase(unittest.TestCase):

    vins = {
        'allowed': [],
        'disallowed': []
    }
    telemetry_points = [
        'bms_pack_soc',
        'humidity',
        'controller_1_inverter_temperature',
        'gps_position[3d:]',
        'ambient_temp[]',
        'speed[1604563200000ms:1604649599999ms]'
    ]

    UNITTEST_ADMIN_USERNAME = arcimoto.tests.unit_test_user_get_username(True)

    @property
    def vin_invalid(self):
        return arcimoto.tests.uuid_vin_get()

    @classmethod
    def setUpClass(cls):
        cls.vin = arcimoto.tests.uuid_vin_get()
        cls.vin2 = arcimoto.tests.uuid_vin_get()
        cls.vin3 = arcimoto.tests.uuid_vin_get()
        arcimoto.tests.vehicle_create(cls.vin)
        arcimoto.tests.vehicle_create(cls.vin2)
        arcimoto.tests.vehicle_create(cls.vin3)
        cls.vehicle_group_id = fleets_functions.vehicle_group_create()
        fleets_functions.vehicle_group_add_user(cls.vehicle_group_id, cls.UNITTEST_ADMIN_USERNAME)
        fleets_functions.vehicle_group_add_vehicle(cls.vehicle_group_id, cls.vin)
        fleets_functions.vehicle_group_add_vehicle(cls.vehicle_group_id, cls.vin2)
        cls.vins['allowed'].extend([cls.vin, cls.vin2])
        cls.vins['disallowed'].append(cls.vin3)

    @classmethod
    def tearDownClass(cls):
        fleets_functions.vehicle_group_delete(cls.vehicle_group_id)
        arcimoto.tests.vehicle_delete(cls.vin)
        arcimoto.tests.vehicle_delete(cls.vin2)
        arcimoto.tests.vehicle_delete(cls.vin3)

    def test_vehicles_telemetry_get_success(self):
        vins_telemetry_points = telemetry_functions.vehicles_telemetry_get(self.vins['allowed'], self.telemetry_points)
        self.assertIsInstance(vins_telemetry_points, dict)

    # test errors
    def test_vehicles_telemetry_get_error_input_invalid_vin(self):
        with self.assertRaises(ArcimotoNotFoundError):
            telemetry_functions.vehicles_telemetry_get([self.vin_invalid], self.telemetry_points)

    def test_vehicles_telemetry_get_error_user_unauthenticated(self):
        with self.assertRaises(ArcimotoPermissionError):
            telemetry_functions.vehicles_telemetry_get(self.vins['allowed'], self.telemetry_points, False)

    def test_vehicles_telemetry_get_error_user_unauthorized_for_vin(self):
        with self.assertRaises(ArcimotoPermissionError):
            telemetry_functions.vehicles_telemetry_get(self.vins['disallowed'], self.telemetry_points)


@arcimoto.runtime.handler
def test_vehicles_telemetry_get():
    return arcimoto.tests.handle_test_result(unittest.TextTestRunner().run(
        unittest.TestLoader().loadTestsFromTestCase(VehiclesTelemetryGetTestCase)
    ))


lambda_handler = test_vehicles_telemetry_get
