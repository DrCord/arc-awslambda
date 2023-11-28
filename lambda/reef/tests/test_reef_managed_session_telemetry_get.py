import logging
import unittest

from arcimoto.exceptions import *
import arcimoto.runtime
import arcimoto.tests
import fleets_functions
import managed_session_functions
import reef_functions

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class ReefManagedSessionTelemetryGetTestCase(unittest.TestCase):

    MODEL_RELEASE_ID = 1
    REEF_VEHICLE_GROUP_ID = reef_functions.REEF_VEHICLE_GROUP_ID
    managed_session_id = None
    vin = None
    vin_not_in_managed_session_mode = None

    @property
    def managed_session_id_invalid(self):
        return reef_functions.managed_sessions_get_highest_id() + 1

    @property
    def vin_invalid(self):
        return arcimoto.tests.uuid_vin_get()

    @classmethod
    def setUpClass(cls):
        # controlled by reef
        cls.vin = arcimoto.tests.uuid_vin_get()
        arcimoto.tests.vehicle_create(cls.vin, cls.MODEL_RELEASE_ID)
        fleets_functions.vehicle_group_add_vehicle(cls.REEF_VEHICLE_GROUP_ID, cls.vin)
        reef_functions.managed_session_mode_set(cls.vin, True)
        cls.managed_session_id = reef_functions.managed_session_start(cls.vin, 'unit_test:reef_managed_session_end').get('id', None)
        if cls.managed_session_id is None:
            raise Exception('Unable to run unit tests: reef_managed_session_start failed in setup')
        reef_functions.managed_session_end(cls.vin)

    @classmethod
    def tearDownClass(cls):
        reef_functions.managed_session_mode_set(cls.vin, False)
        fleets_functions.vehicle_group_remove_vehicle(cls.REEF_VEHICLE_GROUP_ID, cls.vin)
        arcimoto.tests.vehicle_delete(cls.vin)

    def test_reef_managed_session_telemetry_get_success(self):
        self.assertIsInstance(reef_functions.managed_session_telemetry_get(self.managed_session_id), dict)

    # test errors
    def test_reef_managed_session_telemetry_get_error_input_null_id(self):
        with self.assertRaises(ArcimotoArgumentError):
            reef_functions.managed_session_telemetry_get(None)

    def test_reef_managed_session_telemetry_get_error_input_invalid_type_id(self):
        with self.assertRaises(ArcimotoArgumentError):
            reef_functions.managed_session_telemetry_get('not an integer id', None)

    def test_reef_managed_session_telemetry_get_error_input_invalid_id_min(self):
        with self.assertRaises(ArcimotoArgumentError):
            reef_functions.managed_session_telemetry_get(-1)

    def test_reef_managed_session_telemetry_get_error_input_invalid_id(self):
        with self.assertRaises(ArcimotoREEFAlertException):
            reef_functions.managed_session_telemetry_get(self.managed_session_id_invalid)


@arcimoto.runtime.handler
def test_reef_managed_session_telemetry_get():
    return arcimoto.tests.handle_test_result(unittest.TextTestRunner().run(
        unittest.TestLoader().loadTestsFromTestCase(ReefManagedSessionTelemetryGetTestCase)
    ))


lambda_handler = test_reef_managed_session_telemetry_get
