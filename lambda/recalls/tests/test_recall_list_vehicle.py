import logging
import unittest

from arcimoto.exceptions import *
import arcimoto.runtime
import arcimoto.tests
import recall_functions

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class RecallListVehicleTestCase(unittest.TestCase):

    @property
    def vin_invalid(self):
        return arcimoto.tests.uuid_vin_get()

    @classmethod
    def setUpClass(cls):
        cls.test_vin = arcimoto.tests.uuid_vin_get()
        cls.test_vin2 = arcimoto.tests.uuid_vin_get()
        arcimoto.tests.vehicle_create(cls.test_vin)
        arcimoto.tests.vehicle_create(cls.test_vin2)
        cls.recall_id = recall_functions.recall_create()
        recall_functions.recall_add_vehicle({'recall_id': cls.recall_id, 'vins': [cls.test_vin]})
        args = {
            'title': 'TEST-GENERATED-RECALL2',
            'description': 'Generated by unit tests',
            'nhtsa_number': '1234567890',
            'mfr_campaign_id': '0987654321',
            'country': 'USA',
            'safety_recall': True,
            'safety_description': 'Generated by unit test script'
        }
        cls.recall_id2 = recall_functions.recall_create(args)
        recall_functions.recall_add_vehicle({'recall_id': cls.recall_id2, 'vins': [cls.test_vin]})
        recall_functions.recall_add_vehicle({'recall_id': cls.recall_id, 'vins': [cls.test_vin2]})
        recall_functions.recall_delete(cls.recall_id2)
        cls.vehicle_recall_list_test_vin = recall_functions.recall_list_vehicle({'vin': cls.test_vin})
        cls.vehicle_recall_list_len_test_vin = len(cls.vehicle_recall_list_test_vin)
        cls.vehicle_recall_list_all_length = len(recall_functions.recall_list_vehicle({}))
        cls.vehicle_recall_deleted_list = recall_functions.recall_list_vehicle({'vin': cls.test_vin, 'get_deleted_recalls': True})

    @classmethod
    def tearDownClass(cls):
        if cls.recall_id is not None:
            recall_functions.recall_delete(cls.recall_id)
        arcimoto.tests.vehicle_delete(cls.test_vin)
        arcimoto.tests.vehicle_delete(cls.test_vin2)

    def test_recall_list_vehicle_success_input_null(self):
        self.assertTrue(len(recall_functions.recall_list_vehicle({})) > 0)

    def test_recall_list_vehicle_success_input_get_deleted_recalls(self):
        vehicle_recall_deleted_list = recall_functions.recall_list_vehicle({'vin': self.test_vin, 'get_deleted_recalls': True})
        vehicle_recall_deleted_list_length = len(vehicle_recall_deleted_list)
        self.assertTrue(0 < self.vehicle_recall_list_len_test_vin < vehicle_recall_deleted_list_length)

    def test_recall_list_vehicle_success_input_vin_only(self):
        vehicle_recall_list_length = len(recall_functions.recall_list_vehicle({'vin': self.test_vin}))
        self.assertTrue(0 < vehicle_recall_list_length < self.vehicle_recall_list_all_length)

    def test_recall_list_vehicle_success_input_get_recall_data(self):
        self.assertFalse(self.vehicle_recall_list_test_vin[0].get('recall', None))
        vehicle_recall_recall_data_list = recall_functions.recall_list_vehicle({'vin': self.test_vin, 'get_recall_data': True})
        self.assertTrue(vehicle_recall_recall_data_list[0].get('recall', None))

    def test_recall_list_vehicle_success_input_invalid_vin(self):
        # invalid VIN returns empty list
        self.assertTrue(len(recall_functions.recall_list_vehicle({'vin': self.vin_invalid})) == 0)

    # test errors
    def test_recall_list_vehicle_error_input_invalid_type_vin(self):
        with self.assertRaises(ArcimotoArgumentError):
            recall_functions.recall_get_vehicle({'vin': 1})

    def test_recall_list_vehicle_error_input_invalid_type_get_recall_data(self):
        with self.assertRaises(ArcimotoArgumentError):
            recall_functions.recall_get_vehicle({'get_recall_data': 'not a boolean'})

    def test_recall_list_vehicle_error_input_invalid_type_get_deleted_recalls(self):
        with self.assertRaises(ArcimotoArgumentError):
            recall_functions.recall_get_vehicle({'get_deleted_recalls': 'not a boolean'})

    def test_recall_list_vehicle_error_user_unauthorized_input_get_deleted_recalls(self):
        with self.assertRaises(ArcimotoPermissionError):
            recall_functions.recall_list_vehicle({'get_deleted_recalls': True}, False)


@arcimoto.runtime.handler
def test_recall_list_vehicle():

    return arcimoto.tests.handle_test_result(unittest.TextTestRunner().run(
        unittest.TestLoader().loadTestsFromTestCase(RecallListVehicleTestCase)
    ))


lambda_handler = test_recall_list_vehicle
