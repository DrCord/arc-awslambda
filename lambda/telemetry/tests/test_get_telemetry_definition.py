import logging
import unittest


from arcimoto.exceptions import *
import arcimoto.runtime
import arcimoto.tests
import telemetry_functions

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class GetTelemetryDefinitionTestCase(unittest.TestCase):

    @property
    def vin_invalid(self):
        return arcimoto.tests.uuid_vin_get()

    @classmethod
    def setUpClass(cls):
        cls.vin = arcimoto.tests.uuid_vin_get()
        arcimoto.tests.vehicle_create(cls.vin)
        cls.telemetry_definition = telemetry_functions.set_telemetry_version(cls.vin, telemetry_functions.telemetry_get_initial_version())

    @classmethod
    def tearDownClass(cls):
        arcimoto.tests.vehicle_delete(cls.vin)

    def test_get_telemetry_definition_success(self):
        self.assertTrue(telemetry_functions.get_telemetry_definition(self.vin).get('_version', None))

    # test errors
    def test_get_telemetry_definition_error_input_null_vin(self):
        with self.assertRaises(ArcimotoArgumentError):
            telemetry_functions.get_telemetry_definition(None)

    def test_get_telemetry_definition_error_input_invalid_type_vin(self):
        with self.assertRaises(ArcimotoArgumentError):
            telemetry_functions.get_telemetry_definition(1)

    def test_get_telemetry_definition_error_input_invalid_vin(self):
        with self.assertRaises(ArcimotoNotFoundError):
            telemetry_functions.get_telemetry_definition(self.vin_invalid)


@arcimoto.runtime.handler
def test_get_telemetry_definition():
    return arcimoto.tests.handle_test_result(unittest.TextTestRunner().run(
        unittest.TestLoader().loadTestsFromTestCase(GetTelemetryDefinitionTestCase)
    ))


lambda_handler = test_get_telemetry_definition
