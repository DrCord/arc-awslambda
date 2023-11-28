import logging
import unittest


from arcimoto.exceptions import *
import arcimoto.runtime
import arcimoto.tests
import yrisk_functions

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class YriskVehicleTelemetryGetTestCase(unittest.TestCase):

    vin = arcimoto.tests.uuid_vin_get()

    @classmethod
    def setUpClass(cls):
        arcimoto.tests.vehicle_create(cls.vin)

    @classmethod
    def tearDownClass(cls):
        arcimoto.tests.vehicle_delete(cls.vin)

    def test_get_telemetry_vehicle_success(self):
        self.assertIsInstance(yrisk_functions.vehicle_telemetry_get(self.vin), dict)

    # test errors
    def test_get_telemetry_vehicle_error_input_null_vin(self):
        with self.assertRaises(ArcimotoArgumentError):
            yrisk_functions.vehicle_telemetry_get(None)

    def test_get_telemetry_vehicle_error_input_invalid_type_vin(self):
        with self.assertRaises(ArcimotoArgumentError):
            yrisk_functions.vehicle_telemetry_get(1)


@arcimoto.runtime.handler
def test_yrisk_vehicle_telemetry_get():
    return arcimoto.tests.handle_test_result(unittest.TextTestRunner().run(
        unittest.TestLoader().loadTestsFromTestCase(YriskVehicleTelemetryGetTestCase)
    ))


lambda_handler = test_yrisk_vehicle_telemetry_get
