import logging
import unittest


from arcimoto.exceptions import *
import arcimoto.runtime
import arcimoto.tests
import vehicles_functions

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class GpsRecordingToggleTestCase(unittest.TestCase):

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

    def test_gps_recording_toggle_success(self):
        self.assertIsInstance(vehicles_functions.gps_recording_toggle(self.vin, True), dict)
        self.assertIsInstance(vehicles_functions.gps_recording_toggle(self.vin, False), dict)

    # test errors
    def test_gps_recording_toggle_error_input_null_vin(self):
        with self.assertRaises(ArcimotoArgumentError):
            vehicles_functions.gps_recording_toggle(None, True)

    def test_gps_recording_toggle_error_input_null_record_gps(self):
        with self.assertRaises(ArcimotoArgumentError):
            vehicles_functions.gps_recording_toggle(self.vin, None)

    def test_gps_recording_toggle_error_input_invalid_vin(self):
        with self.assertRaises(ArcimotoNotFoundError):
            vehicles_functions.gps_recording_toggle(self.vin_invalid, True)

    def test_gps_recording_toggle_error_input_invalid_type_vin(self):
        with self.assertRaises(ArcimotoArgumentError):
            vehicles_functions.gps_recording_toggle(1, True)

    def test_gps_recording_toggle_error_user_unauthorized(self):
        with self.assertRaises(ArcimotoPermissionError):
            vehicles_functions.gps_recording_toggle(self.vin, True, False)


@arcimoto.runtime.handler
def test_gps_recording_toggle():
    return arcimoto.tests.handle_test_result(unittest.TextTestRunner().run(
        unittest.TestLoader().loadTestsFromTestCase(GpsRecordingToggleTestCase)
    ))


lambda_handler = test_gps_recording_toggle
