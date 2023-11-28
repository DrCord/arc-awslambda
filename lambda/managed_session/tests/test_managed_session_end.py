import logging
import unittest

from arcimoto.exceptions import *
import arcimoto.runtime
import arcimoto.tests
import managed_session_functions

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class ManagedSessionEndTestCase(unittest.TestCase):

    MODEL_RELEASE_ID = 1
    vin = None
    vin_not_in_managed_session_mode = None

    @property
    def vin_invalid(self):
        return arcimoto.tests.uuid_vin_get()

    @classmethod
    def setUpClass(cls):
        cls.vin = arcimoto.tests.uuid_vin_get()
        arcimoto.tests.vehicle_create(cls.vin, cls.MODEL_RELEASE_ID)
        managed_session_functions.mode_set(cls.vin, True)
        managed_session_functions.start(cls.vin, 'unit_test:managed_session_end')

        cls.vin_not_in_managed_session_mode = arcimoto.tests.uuid_vin_get()
        arcimoto.tests.vehicle_create(cls.vin_not_in_managed_session_mode, cls.MODEL_RELEASE_ID)

    @classmethod
    def tearDownClass(cls):
        managed_session_functions.mode_set(cls.vin, False)
        arcimoto.tests.vehicle_delete(cls.vin)
        arcimoto.tests.vehicle_delete(cls.vin_not_in_managed_session_mode)

    def test_managed_session_end_success(self):
        self.assertIsInstance(managed_session_functions.end(self.vin), dict)

    # test errors
    def test_managed_session_end_error_input_null_vin(self):
        with self.assertRaises(ArcimotoArgumentError):
            managed_session_functions.end(None)

    def test_managed_session_end_error_input_invalid_vin(self):
        with self.assertRaises(ArcimotoNotFoundError):
            managed_session_functions.end(self.vin_invalid)

    def test_managed_session_end_error_input_invalid_type_vin(self):
        with self.assertRaises(ArcimotoArgumentError):
            managed_session_functions.end(1)

    def test_managed_session_end_error_input_vin_not_in_managed_session_mode(self):
        with self.assertRaises(ArcimotoException):
            managed_session_functions.end(self.vin_not_in_managed_session_mode)

    def test_managed_session_end_error_unauthorized(self):
        with self.assertRaises(ArcimotoPermissionError):
            managed_session_functions.end(self.vin, False)


@arcimoto.runtime.handler
def test_managed_session_end():
    return arcimoto.tests.handle_test_result(unittest.TextTestRunner().run(
        unittest.TestLoader().loadTestsFromTestCase(ManagedSessionEndTestCase)
    ))


lambda_handler = test_managed_session_end
