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


class ReefManagedSessionGetTestCase(unittest.TestCase):

    MODEL_RELEASE_ID = 1
    REEF_VEHICLE_GROUP_ID = reef_functions.REEF_VEHICLE_GROUP_ID
    managed_session_id = None
    vin = None

    @property
    def vin_invalid(self):
        return arcimoto.tests.uuid_vin_get()

    @classmethod
    def setUpClass(cls):
        # controlled by REEF vehicle group
        cls.vin = arcimoto.tests.uuid_vin_get()
        arcimoto.tests.vehicle_create(cls.vin, cls.MODEL_RELEASE_ID)
        fleets_functions.vehicle_group_add_vehicle(cls.REEF_VEHICLE_GROUP_ID, cls.vin)
        reef_functions.managed_session_mode_set(cls.vin, True)
        cls.managed_session_id = reef_functions.managed_session_start(cls.vin, 'unit_test:reef_managed_session_get').get('id', None)
        if cls.managed_session_id is None:
            raise Exception('Unable to run unit tests: reef_managed_session_start failed in setup')
        reef_functions.managed_session_end(cls.vin)

    @classmethod
    def tearDownClass(cls):
        reef_functions.managed_session_mode_set(cls.vin, False)
        fleets_functions.vehicle_group_remove_vehicle(cls.REEF_VEHICLE_GROUP_ID, cls.vin)
        arcimoto.tests.vehicle_delete(cls.vin)

    def test_reef_managed_session_get_success_input_id(self):
        self.assertIsInstance(reef_functions.managed_session_get(self.managed_session_id, None), dict)

    def test_reef_managed_session_get_success_input_vin(self):
        self.assertIsInstance(reef_functions.managed_session_get(None, self.vin), dict)

    # test errors
    def test_reef_managed_session_get_error_input_null_params(self):
        with self.assertRaises(ArcimotoArgumentError):
            reef_functions.managed_session_get()

    def test_reef_managed_session_get_error_input_invalid_type_id(self):
        with self.assertRaises(ArcimotoArgumentError):
            reef_functions.managed_session_get('not an integer id', None)

    def test_reef_managed_session_get_error_input_invalid_type_vin(self):
        with self.assertRaises(ArcimotoArgumentError):
            reef_functions.managed_session_get(None, 1)

    def test_reef_managed_session_get_error_input_invalid_id_min(self):
        with self.assertRaises(ArcimotoArgumentError):
            reef_functions.managed_session_get(0, None)

    # unauthorized check comes before vin validity check, so invalid VINs are unauthorized
    def test_reef_managed_session_get_error_unauthorized_for_vin(self):
        with self.assertRaises(ArcimotoPermissionError):
            reef_functions.managed_session_get(None, self.vin_invalid)

    def test_reef_managed_session_get_error_input_invalid_vin(self):
        invalid_allowed_vin = self.vin_invalid
        reef_functions.add_invalid_vin_directly_to_vehicle_group(invalid_allowed_vin)
        with self.assertRaises(ArcimotoNotFoundError):
            reef_functions.managed_session_get(None, invalid_allowed_vin)
        reef_functions.remove_invalid_vin_directly_from_vehicle_group(invalid_allowed_vin)


@arcimoto.runtime.handler
def test_reef_managed_session_get():
    return arcimoto.tests.handle_test_result(unittest.TextTestRunner().run(
        unittest.TestLoader().loadTestsFromTestCase(ReefManagedSessionGetTestCase)
    ))


lambda_handler = test_reef_managed_session_get
