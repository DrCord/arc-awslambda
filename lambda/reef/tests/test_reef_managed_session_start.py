import logging
import unittest

from arcimoto.exceptions import *
import arcimoto.runtime
import arcimoto.tests
import fleets_functions
import reef_functions

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class ReefManagedSessionStartTestCase(unittest.TestCase):

    MODEL_RELEASE_ID = 1
    REEF_VEHICLE_GROUP_ID = reef_functions.REEF_VEHICLE_GROUP_ID
    vin = None
    vin_not_in_managed_session_mode = None
    verification_id = 'unit_test:reef_managed_session_start'

    @property
    def vin_invalid(self):
        return arcimoto.tests.uuid_vin_get()

    @classmethod
    def setUpClass(cls):
        cls.vin = arcimoto.tests.uuid_vin_get()
        arcimoto.tests.vehicle_create(cls.vin, cls.MODEL_RELEASE_ID)
        fleets_functions.vehicle_group_add_vehicle(cls.REEF_VEHICLE_GROUP_ID, cls.vin)
        reef_functions.managed_session_mode_set(cls.vin, True)

        cls.vin_not_in_managed_session_mode = arcimoto.tests.uuid_vin_get()
        arcimoto.tests.vehicle_create(cls.vin_not_in_managed_session_mode, cls.MODEL_RELEASE_ID)
        fleets_functions.vehicle_group_add_vehicle(cls.REEF_VEHICLE_GROUP_ID, cls.vin_not_in_managed_session_mode)

    @classmethod
    def tearDownClass(cls):
        reef_functions.managed_session_end(cls.vin)
        reef_functions.managed_session_mode_set(cls.vin, False)
        fleets_functions.vehicle_group_remove_vehicle(cls.REEF_VEHICLE_GROUP_ID, cls.vin)
        arcimoto.tests.vehicle_delete(cls.vin)

        fleets_functions.vehicle_group_remove_vehicle(cls.REEF_VEHICLE_GROUP_ID, cls.vin_not_in_managed_session_mode)
        arcimoto.tests.vehicle_delete(cls.vin_not_in_managed_session_mode)

    def test_managed_session_start_success(self):
        self.assertIsInstance(reef_functions.managed_session_start(self.vin, self.verification_id), dict)

    # test errors
    def test_managed_session_start_error_input_null_vin(self):
        with self.assertRaises(ArcimotoArgumentError):
            reef_functions.managed_session_start(None, self.verification_id)

    def test_managed_session_start_error_input_null_verification_id(self):
        with self.assertRaises(ArcimotoArgumentError):
            reef_functions.managed_session_start(self.vin, None)

    def test_managed_session_start_error_input_invalid_type_vin(self):
        with self.assertRaises(ArcimotoArgumentError):
            reef_functions.managed_session_start(1, self.verification_id)

    def test_managed_session_start_error_input_invalid_type_verification_id(self):
        with self.assertRaises(ArcimotoArgumentError):
            reef_functions.managed_session_start(self.vin, 1)

    def test_managed_session_start_error_input_empty_verification_id(self):
        with self.assertRaises(ArcimotoArgumentError):
            reef_functions.managed_session_start(self.vin, '')

    def test_managed_session_start_error_input_vin_not_in_managed_session_mode(self):
        with self.assertRaises(ArcimotoREEFAlertException):
            reef_functions.managed_session_start(self.vin_not_in_managed_session_mode, self.verification_id)

    # unauthorized check comes before vin validity check, so invalid VINs are unauthorized
    def test_reef_managed_session_start_error_unauthorized_for_vin(self):
        with self.assertRaises(ArcimotoPermissionError):
            reef_functions.managed_session_start(self.vin_invalid, self.verification_id)

    def test_reef_managed_session_start_error_input_invalid_vin(self):
        invalid_allowed_vin = self.vin_invalid
        reef_functions.add_invalid_vin_directly_to_vehicle_group(invalid_allowed_vin)
        with self.assertRaises(ArcimotoNotFoundError):
            reef_functions.managed_session_start(invalid_allowed_vin, self.verification_id)
        reef_functions.remove_invalid_vin_directly_from_vehicle_group(invalid_allowed_vin)


@arcimoto.runtime.handler
def test_managed_session_start():
    return arcimoto.tests.handle_test_result(unittest.TextTestRunner().run(
        unittest.TestLoader().loadTestsFromTestCase(ReefManagedSessionStartTestCase)
    ))


lambda_handler = test_managed_session_start
