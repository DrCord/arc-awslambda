import logging
import unittest

from arcimoto.exceptions import *
import arcimoto.runtime
import arcimoto.tests
import managed_session_functions

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class ManagedSessionGetTestCase(unittest.TestCase):

    MODEL_RELEASE_ID = 1
    managed_session_id = None
    vin = None

    @property
    def vin_invalid(self):
        return arcimoto.tests.uuid_vin_get()

    @classmethod
    def setUpClass(cls):
        cls.vin = arcimoto.tests.uuid_vin_get()
        arcimoto.tests.vehicle_create(cls.vin, cls.MODEL_RELEASE_ID)
        cls.managed_session_id = 2

    @classmethod
    def tearDownClass(cls):
        arcimoto.tests.vehicle_delete(cls.vin)

    def test_managed_session_get_success_input_id(self):
        self.assertIsInstance(managed_session_functions.get(self.managed_session_id, None), dict)

    def test_managed_session_get_success_input_vin(self):
        self.assertIsInstance(managed_session_functions.get(None, self.vin), dict)

    # test errors
    def test_managed_session_get_error_input_null_params(self):
        with self.assertRaises(ArcimotoArgumentError):
            managed_session_functions.get()

    def test_managed_session_get_error_input_invalid_vin(self):
        with self.assertRaises(ArcimotoNotFoundError):
            managed_session_functions.get(None, self.vin_invalid)

    def test_managed_session_get_error_input_invalid_type_id(self):
        with self.assertRaises(ArcimotoArgumentError):
            managed_session_functions.get('not an integer id', None)

    def test_managed_session_get_error_input_invalid_type_vin(self):
        with self.assertRaises(ArcimotoArgumentError):
            managed_session_functions.get(None, 1)

    def test_managed_session_get_error_input_invalid_id_min(self):
        with self.assertRaises(ArcimotoArgumentError):
            managed_session_functions.get(0, None)

    def test_managed_session_get_error_unauthorized(self):
        with self.assertRaises(ArcimotoPermissionError):
            managed_session_functions.get(self.managed_session_id, None, False)


@arcimoto.runtime.handler
def test_managed_session_get():
    return arcimoto.tests.handle_test_result(unittest.TextTestRunner().run(
        unittest.TestLoader().loadTestsFromTestCase(ManagedSessionGetTestCase)
    ))


lambda_handler = test_managed_session_get
