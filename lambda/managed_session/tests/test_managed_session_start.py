import logging
import unittest

from arcimoto.exceptions import *
import arcimoto.runtime
import arcimoto.tests
import managed_session_functions

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class ManagedSessionStartTestCase(unittest.TestCase):

    MODEL_RELEASE_ID = 1
    vin = None
    vin_not_in_managed_session_mode = None
    verification_id = 'unit_test'
    pin = '123456'

    @property
    def vin_invalid(self):
        return arcimoto.tests.uuid_vin_get()

    @classmethod
    def setUpClass(cls):
        cls.vin = arcimoto.tests.uuid_vin_get()
        arcimoto.tests.vehicle_create(cls.vin, cls.MODEL_RELEASE_ID)
        managed_session_functions.mode_set(cls.vin, True)

        cls.vin_not_in_managed_session_mode = arcimoto.tests.uuid_vin_get()
        arcimoto.tests.vehicle_create(cls.vin_not_in_managed_session_mode, cls.MODEL_RELEASE_ID)

    @classmethod
    def tearDownClass(cls):
        managed_session_functions.end(cls.vin)
        managed_session_functions.mode_set(cls.vin, False)
        arcimoto.tests.vehicle_delete(cls.vin)
        arcimoto.tests.vehicle_delete(cls.vin_not_in_managed_session_mode)

    def test_managed_session_start_success(self):
        self.assertIsInstance(managed_session_functions.start(self.vin, self.verification_id), dict)

    def test_managed_session_start_success_with_pin(self):
        self.assertIsInstance(managed_session_functions.start(self.vin, self.verification_id, self.pin), dict)

    # test errors
    def test_managed_session_start_error_input_null_vin(self):
        with self.assertRaises(ArcimotoArgumentError):
            managed_session_functions.start(None, self.verification_id)

    def test_managed_session_start_error_input_invalid_type_vin(self):
        with self.assertRaises(ArcimotoArgumentError):
            managed_session_functions.start(1, self.verification_id)

    def test_managed_session_start_error_input_invalid_type_verification_id(self):
        with self.assertRaises(ArcimotoArgumentError):
            managed_session_functions.start(self.vin, 1)

    def test_managed_session_start_error_input_invalid_vin(self):
        with self.assertRaises(ArcimotoNotFoundError):
            managed_session_functions.start(self.vin_invalid, self.verification_id)

    def test_managed_session_start_error_input_vin_not_in_managed_session_mode(self):
        with self.assertRaises(ArcimotoException):
            managed_session_functions.start(self.vin_not_in_managed_session_mode, self.verification_id)

    def test_managed_session_start_error_input_invalid_pin_too_short(self):
        with self.assertRaises(ArcimotoArgumentError):
            managed_session_functions.start(self.vin, self.verification_id, '123')

    def test_managed_session_start_error_input_invalid_pin_too_long(self):
        with self.assertRaises(ArcimotoArgumentError):
            managed_session_functions.start(self.vin, self.verification_id, '123456789')

    def test_managed_session_start_error_input_invalid_pin_not_numeric(self):
        with self.assertRaises(ArcimotoArgumentError):
            managed_session_functions.start(self.vin, self.verification_id, '1a2b3c')

    def test_managed_session_start_error_unauthorized(self):
        with self.assertRaises(ArcimotoPermissionError):
            managed_session_functions.start(self.vin, self.verification_id, None, False)


@arcimoto.runtime.handler
def test_managed_session_start():
    return arcimoto.tests.handle_test_result(unittest.TextTestRunner().run(
        unittest.TestLoader().loadTestsFromTestCase(ManagedSessionStartTestCase)
    ))


lambda_handler = test_managed_session_start
