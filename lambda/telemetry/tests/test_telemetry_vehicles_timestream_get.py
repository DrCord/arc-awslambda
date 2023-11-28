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


class TelemetryVehiclesTimestreamGetTestCase(unittest.TestCase):

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

    # This set of unit tests fails (in the pipeline only) when setUpClass is used to instantiate resources,
    # so set up and teardown is handled in each test individually

    def test_telemetry_vehicles_timestream_get_success(self):
        # set up
        vins_allowed = []
        vin1 = arcimoto.tests.uuid_vin_get()
        vin2 = arcimoto.tests.uuid_vin_get()
        arcimoto.tests.vehicle_create(vin1)
        arcimoto.tests.vehicle_create(vin2)
        vehicle_group_id = fleets_functions.vehicle_group_create()
        fleets_functions.vehicle_group_add_user(vehicle_group_id, self.UNITTEST_ADMIN_USERNAME)
        fleets_functions.vehicle_group_add_vehicle(vehicle_group_id, vin1)
        fleets_functions.vehicle_group_add_vehicle(vehicle_group_id, vin2)
        vins_allowed.extend([vin1, vin2])
        # test
        vins_telemetry_points = telemetry_functions.telemetry_vehicles_timestream_get(
            vins_allowed,
            self.telemetry_points
        )
        self.assertIsInstance(vins_telemetry_points, dict)
        # clean up
        fleets_functions.vehicle_group_delete(vehicle_group_id)
        arcimoto.tests.vehicle_delete(vin1)
        arcimoto.tests.vehicle_delete(vin2)

    # test errors
    def test_telemetry_vehicles_timestream_get_error_input_invalid_vin(self):
        with self.assertRaises(ArcimotoNotFoundError):
            telemetry_functions.telemetry_vehicles_timestream_get(
                [self.vin_invalid],
                self.telemetry_points
            )

    def test_telemetry_vehicles_timestream_get_error_user_unauthenticated(self):
        # set up
        vins_allowed = []
        vin1 = arcimoto.tests.uuid_vin_get()
        vin2 = arcimoto.tests.uuid_vin_get()
        arcimoto.tests.vehicle_create(vin1)
        arcimoto.tests.vehicle_create(vin2)
        vehicle_group_id = fleets_functions.vehicle_group_create()
        fleets_functions.vehicle_group_add_user(vehicle_group_id, self.UNITTEST_ADMIN_USERNAME)
        fleets_functions.vehicle_group_add_vehicle(vehicle_group_id, vin1)
        fleets_functions.vehicle_group_add_vehicle(vehicle_group_id, vin2)
        vins_allowed.extend([vin1, vin2])
        # test
        with self.assertRaises(ArcimotoPermissionError):
            telemetry_functions.telemetry_vehicles_timestream_get(
                vins_allowed,
                self.telemetry_points,
                False
            )
        # clean up
        fleets_functions.vehicle_group_delete(vehicle_group_id)
        arcimoto.tests.vehicle_delete(vin1)
        arcimoto.tests.vehicle_delete(vin2)

    def test_telemetry_vehicles_timestream_get_error_user_unauthorized_for_vin(self):
        # set up
        vin_disallowed = arcimoto.tests.uuid_vin_get()
        arcimoto.tests.vehicle_create(vin_disallowed)
        # test
        with self.assertRaises(ArcimotoPermissionError):
            telemetry_functions.telemetry_vehicles_timestream_get(
                [vin_disallowed],
                self.telemetry_points
            )
        # clean up
        arcimoto.tests.vehicle_delete(vin_disallowed)


@arcimoto.runtime.handler
def test_telemetry_vehicles_timestream_get():
    return arcimoto.tests.handle_test_result(unittest.TextTestRunner().run(
        unittest.TestLoader().loadTestsFromTestCase(TelemetryVehiclesTimestreamGetTestCase)
    ))


lambda_handler = test_telemetry_vehicles_timestream_get
