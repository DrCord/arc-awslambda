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


class ReefManagedSessionEndTestCase(unittest.TestCase):

    MODEL_RELEASE_ID = 1
    REEF_VEHICLE_GROUP_ID = reef_functions.REEF_VEHICLE_GROUP_ID
    vin = None
    vin_not_in_managed_session_mode = None

    @property
    def vin_invalid(self):
        return arcimoto.tests.uuid_vin_get()

    @classmethod
    def setUpClass(cls):
        cls.vin = arcimoto.tests.uuid_vin_get()
        arcimoto.tests.vehicle_create(cls.vin, cls.MODEL_RELEASE_ID)
        fleets_functions.vehicle_group_add_vehicle(cls.REEF_VEHICLE_GROUP_ID, cls.vin)
        reef_functions.managed_session_mode_set(cls.vin, True)
        reef_functions.managed_session_start(cls.vin, 'unit_test:reef_managed_session_end')

        cls.vin_not_in_managed_session_mode = arcimoto.tests.uuid_vin_get()
        arcimoto.tests.vehicle_create(cls.vin_not_in_managed_session_mode, cls.MODEL_RELEASE_ID)
        fleets_functions.vehicle_group_add_vehicle(cls.REEF_VEHICLE_GROUP_ID, cls.vin_not_in_managed_session_mode)

    @classmethod
    def tearDownClass(cls):
        reef_functions.managed_session_mode_set(cls.vin, False)
        fleets_functions.vehicle_group_remove_vehicle(cls.REEF_VEHICLE_GROUP_ID, cls.vin)
        arcimoto.tests.vehicle_delete(cls.vin)
        fleets_functions.vehicle_group_remove_vehicle(cls.REEF_VEHICLE_GROUP_ID, cls.vin_not_in_managed_session_mode)
        arcimoto.tests.vehicle_delete(cls.vin_not_in_managed_session_mode)

    def test_reef_managed_session_end_success(self):
        self.assertIsInstance(reef_functions.managed_session_end(self.vin), dict)

    # test errors
    def test_reef_managed_session_end_error_input_null_vin(self):
        with self.assertRaises(ArcimotoArgumentError):
            reef_functions.managed_session_end(None)

    def test_reef_managed_session_end_error_input_invalid_type_vin(self):
        with self.assertRaises(ArcimotoArgumentError):
            reef_functions.managed_session_end(1)

    def test_reef_managed_session_end_error_input_vin_not_in_managed_session_mode(self):
        with self.assertRaises(ArcimotoREEFAlertException):
            reef_functions.managed_session_end(self.vin_not_in_managed_session_mode)

    # unauthorized check comes before vin validity check, so invalid VINs are unauthorized
    def test_reef_managed_session_end_error_unauthorized_for_vin(self):
        with self.assertRaises(ArcimotoPermissionError):
            reef_functions.managed_session_end(self.vin_invalid)

    def test_reef_managed_session_end_error_input_invalid_vin(self):
        invalid_allowed_vin = self.vin_invalid
        reef_functions.add_invalid_vin_directly_to_vehicle_group(invalid_allowed_vin)
        with self.assertRaises(ArcimotoNotFoundError):
            reef_functions.managed_session_end(invalid_allowed_vin)
        reef_functions.remove_invalid_vin_directly_from_vehicle_group(invalid_allowed_vin)


@arcimoto.runtime.handler
def test_reef_managed_session_end():
    return arcimoto.tests.handle_test_result(unittest.TextTestRunner().run(
        unittest.TestLoader().loadTestsFromTestCase(ReefManagedSessionEndTestCase)
    ))


lambda_handler = test_reef_managed_session_end
