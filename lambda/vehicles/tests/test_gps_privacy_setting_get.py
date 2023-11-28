import logging
import unittest


from arcimoto.exceptions import *
import arcimoto.runtime
import arcimoto.tests
import vehicles_functions

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class GpsPrivacySettingGetTestCase(unittest.TestCase):

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

    def test_gps_privacy_setting_get_success(self):
        vehicles_functions.gps_recording_toggle(self.vin, True)
        self.assertTrue(vehicles_functions.gps_privacy_setting_get(self.vin).get('record_gps', None))
        vehicles_functions.gps_recording_toggle(self.vin, False)
        self.assertFalse(vehicles_functions.gps_privacy_setting_get(self.vin).get('record_gps', None))

    # test errors
    def test_gps_privacy_setting_get_error_input_null_vin(self):
        with self.assertRaises(ArcimotoArgumentError):
            vehicles_functions.gps_privacy_setting_get(None)

    def test_gps_privacy_setting_get_error_input_invalid_type_vin(self):
        with self.assertRaises(ArcimotoArgumentError):
            vehicles_functions.gps_privacy_setting_get(1)

    def test_gps_privacy_setting_get_error_input_invalid_vin(self):
        with self.assertRaises(ArcimotoNotFoundError):
            vehicles_functions.gps_privacy_setting_get(self.vin_invalid)

    def test_gps_privacy_setting_get_error_user_unauthorized(self):
        with self.assertRaises(ArcimotoPermissionError):
            vehicles_functions.gps_privacy_setting_get(self.vin, False)


@arcimoto.runtime.handler
def test_gps_privacy_setting_get():
    return arcimoto.tests.handle_test_result(unittest.TextTestRunner().run(
        unittest.TestLoader().loadTestsFromTestCase(GpsPrivacySettingGetTestCase)
    ))


lambda_handler = test_gps_privacy_setting_get
