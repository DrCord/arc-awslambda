import logging
import unittest


from arcimoto.exceptions import *
import arcimoto.runtime
import arcimoto.tests
import telemetry_functions
import vehicles_functions

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class ShadowReportedStateTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.vin = arcimoto.tests.uuid_vin_get()
        arcimoto.tests.vehicle_create(cls.vin)
        vehicles_functions.provision_iot(cls.vin)
        certificates = vehicles_functions.provision_iot_certificate(cls.vin)
        cls.reported = {
            'telemetry_version': telemetry_functions.telemetry_get_initial_version(),
            'record_gps': True,
            'telemetry_points': telemetry_functions.telemetry_points_get_defaults(),
            'trusted_keys': [
                certificates.get('certificate_pem', None)
            ]
        }

    @classmethod
    def tearDownClass(cls):
        vehicles_functions.unprovision_iot_certificate(cls.vin)
        vehicles_functions.unprovision_iot(cls.vin)
        arcimoto.tests.vehicle_delete(cls.vin)

    def test_shadow_reported_state_success(self):
        self.assertIsInstance(vehicles_functions.shadow_reported_state(self.vin, self.reported), dict)

    # test errors
    def test_shadow_reported_state_error_input_null_vin(self):
        with self.assertRaises(ArcimotoArgumentError):
            vehicles_functions.shadow_reported_state(None, self.reported)

    def test_shadow_reported_state_error_input_null_reported(self):
        with self.assertRaises(ArcimotoArgumentError):
            vehicles_functions.shadow_reported_state(self.vin, None)

    def test_shadow_reported_state_error_input_invalid_type_vin(self):
        with self.assertRaises(ArcimotoArgumentError):
            vehicles_functions.shadow_reported_state(1, self.reported)

    def test_shadow_reported_state_error_input_invalid_type_reported(self):
        with self.assertRaises(ArcimotoArgumentError):
            vehicles_functions.shadow_reported_state(self.vin, 'not a dictionary')


@arcimoto.runtime.handler
def test_shadow_reported_state():
    return arcimoto.tests.handle_test_result(unittest.TextTestRunner().run(
        unittest.TestLoader().loadTestsFromTestCase(ShadowReportedStateTestCase)
    ))


lambda_handler = test_shadow_reported_state
