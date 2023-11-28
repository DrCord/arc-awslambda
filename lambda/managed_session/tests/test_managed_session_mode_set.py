import logging
import unittest

from arcimoto.exceptions import *
import arcimoto.runtime
import arcimoto.tests
import managed_session_functions

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class ManagedSessionModeSetTestCase(unittest.TestCase):

    MODEL_RELEASE_ID = 1
    vin = None
    managed_session_mode = None

    @property
    def vin_invalid(self):
        return arcimoto.tests.uuid_vin_get()

    @classmethod
    def setUpClass(cls):
        cls.vin = arcimoto.tests.uuid_vin_get()
        arcimoto.tests.vehicle_create(cls.vin, cls.MODEL_RELEASE_ID)
        cls.managed_session_mode = True

    @classmethod
    def tearDownClass(cls):
        arcimoto.tests.vehicle_delete(cls.vin)

    def test_managed_session_mode_set_success_no_mode(self):
        self.assertIsInstance(managed_session_functions.mode_set(self.vin), dict)

    def test_managed_session_mode_set_success_mode_true(self):
        self.assertIsInstance(managed_session_functions.mode_set(self.vin, self.managed_session_mode), dict)

    def test_managed_session_mode_set_success_mode_false(self):
        self.assertIsInstance(managed_session_functions.mode_set(self.vin, False), dict)

    # test errors
    def test_managed_session_mode_set_error_input_null_vin(self):
        with self.assertRaises(ArcimotoArgumentError):
            managed_session_functions.mode_set(None)

    def test_managed_session_mode_set_error_input_invalid_vin(self):
        with self.assertRaises(ArcimotoNotFoundError):
            managed_session_functions.mode_set(self.vin_invalid)

    def test_managed_session_mode_set_error_input_invalid_type_vin(self):
        with self.assertRaises(ArcimotoArgumentError):
            managed_session_functions.mode_set(1)

    def test_managed_session_mode_set_error_unauthorized(self):
        with self.assertRaises(ArcimotoPermissionError):
            managed_session_functions.mode_set(self.vin, self.managed_session_mode, False)


@arcimoto.runtime.handler
def test_managed_session_mode_set():
    return arcimoto.tests.handle_test_result(unittest.TextTestRunner().run(
        unittest.TestLoader().loadTestsFromTestCase(ManagedSessionModeSetTestCase)
    ))


lambda_handler = test_managed_session_mode_set
