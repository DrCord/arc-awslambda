import logging
import unittest

from arcimoto.exceptions import *
import arcimoto.runtime
import arcimoto.tests
import recall_functions

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class RecallServiceVehicleTestCase(unittest.TestCase):

    @property
    def recall_id_invalid(self):
        return recall_functions.recalls_get_highest_id() + 1

    @property
    def vehicle_recall_id_invalid(self):
        return recall_functions.vehicle_recalls_get_highest_id() + 1

    @property
    def vin_invalid(self):
        return arcimoto.tests.uuid_vin_get()

    @classmethod
    def setUpClass(cls):
        cls.vin = arcimoto.tests.uuid_vin_get()
        cls.vin2 = arcimoto.tests.uuid_vin_get()
        cls.vin3 = arcimoto.tests.uuid_vin_get()
        cls.vin4 = arcimoto.tests.uuid_vin_get()
        cls.vin5 = arcimoto.tests.uuid_vin_get()
        cls.vin6 = arcimoto.tests.uuid_vin_get()
        arcimoto.tests.vehicle_create(cls.vin)
        arcimoto.tests.vehicle_create(cls.vin2)
        arcimoto.tests.vehicle_create(cls.vin3)
        arcimoto.tests.vehicle_create(cls.vin4)
        arcimoto.tests.vehicle_create(cls.vin5)
        arcimoto.tests.vehicle_create(cls.vin6)
        cls.recall_id = recall_functions.recall_create()

    @classmethod
    def tearDownClass(cls):
        if cls.recall_id is not None:
            recall_functions.recall_delete(cls.recall_id)
        arcimoto.tests.vehicle_delete(cls.vin)
        arcimoto.tests.vehicle_delete(cls.vin2)
        arcimoto.tests.vehicle_delete(cls.vin3)
        arcimoto.tests.vehicle_delete(cls.vin4)
        arcimoto.tests.vehicle_delete(cls.vin5)
        arcimoto.tests.vehicle_delete(cls.vin6)

    def test_recall_service_vehicle_success_input_vehicle_recall_id(self):
        recall_add_vehicle_args = {
            'recall_id': self.recall_id,
            'vins': [self.vin]
        }
        vehicle_recall = recall_functions.recall_add_vehicle(recall_add_vehicle_args)
        vehicle_recall_id = vehicle_recall.get('vehicle_recall_ids')[0]
        recall_service_vehicle_args = {
            'vehicle_recall_id': vehicle_recall_id
        }
        self.assertIsInstance(recall_functions.recall_service_vehicle(recall_service_vehicle_args), dict)

    def test_recall_service_vehicle_success_input_recall_id_and_single_vin(self):
        recall_add_vehicle_args = {
            'recall_id': self.recall_id,
            'vins': [self.vin2]
        }
        recall_functions.recall_add_vehicle(recall_add_vehicle_args)
        recall_service_vehicle_args = {
            'recall_id': self.recall_id,
            'vins': [self.vin2]
        }
        self.assertIsInstance(recall_functions.recall_service_vehicle(recall_service_vehicle_args), dict)

    def test_recall_service_vehicle_success_input_recall_id_and_multiple_vins(self):
        recall_add_vehicle_args = {
            'recall_id': self.recall_id,
            'vins': [
                self.vin5,
                self.vin6
            ]
        }
        recall_functions.recall_add_vehicle(recall_add_vehicle_args)
        recall_service_vehicle_args = {
            'recall_id': self.recall_id,
            'vins': [
                self.vin5,
                self.vin6
            ]
        }
        self.assertIsInstance(recall_functions.recall_service_vehicle(recall_service_vehicle_args), dict)

    def test_recall_service_vehicle_success_input_vehicle_recall_id_with_service_reference(self):
        recall_add_vehicle_args = {
            'recall_id': self.recall_id,
            'vins': [
                self.vin3
            ]
        }
        vehicle_recall = recall_functions.recall_add_vehicle(recall_add_vehicle_args)
        vehicle_recall_id = vehicle_recall.get('vehicle_recall_ids')[0]
        recall_service_vehicle_args = {
            'vehicle_recall_id': vehicle_recall_id,
            'service_reference': 'unit-test:test_recall_service_vehicle_success_input_vehicle_recall_id_with_service_reference'
        }
        self.assertIsInstance(recall_functions.recall_service_vehicle(recall_service_vehicle_args), dict)

    def test_recall_service_vehicle_success_input_recall_id_and_vin_with_service_reference(self):
        recall_add_vehicle_args = {
            'recall_id': self.recall_id,
            'vins': [
                self.vin4
            ]
        }
        recall_functions.recall_add_vehicle(recall_add_vehicle_args)
        recall_service_vehicle_args = {
            'recall_id': self.recall_id,
            'vins': [
                self.vin4
            ],
            'service_reference': 'unit-test:test_recall_service_vehicle_success_input_recall_id_and_vin_with_service_reference'
        }
        self.assertIsInstance(recall_functions.recall_service_vehicle(recall_service_vehicle_args), dict)

    # test errors
    def test_recall_service_vehicle_error_input_null_recall_id(self):
        with self.assertRaises(ArcimotoArgumentError):
            recall_functions.recall_service_vehicle({'recall_id': None, 'vins': [self.vin]})

    def test_recall_service_vehicle_error_input_null_vin(self):
        with self.assertRaises(ArcimotoArgumentError):
            recall_functions.recall_service_vehicle({'recall_id': self.recall_id, 'vins': None})

    def test_recall_service_vehicle_error_invalid_vehicle_recall_id(self):
        with self.assertRaises(ArcimotoArgumentError):
            recall_functions.recall_service_vehicle({'vehicle_recall_id': self.vehicle_recall_id_invalid})

    def test_recall_service_vehicle_error_invalid_recall_id(self):
        with self.assertRaises(ArcimotoArgumentError):
            recall_functions.recall_service_vehicle({'recall_id': self.recall_id_invalid, 'vins': [self.vin]})

    def test_recall_service_vehicle_error_invalid_vin(self):
        with self.assertRaises(ArcimotoArgumentError):
            recall_functions.recall_service_vehicle({'recall_id': self.recall_id, 'vins': [self.vin_invalid]})

    def test_recall_service_vehicle_error_input_invalid_type_vehicle_recall_id(self):
        with self.assertRaises(ArcimotoArgumentError):
            recall_functions.recall_service_vehicle({'vehicle_recall_id': 'not an integer'})

    def test_recall_service_vehicle_error_input_invalid_type_recall_id(self):
        args = {
            'recall_id': 'not an integer',
            'vins': [self.vin2]
        }
        with self.assertRaises(ArcimotoArgumentError):
            recall_functions.recall_service_vehicle(args)

    def test_recall_service_vehicle_error_input_invalid_type_vin(self):
        args = {
            'recall_id': self.recall_id,
            'vins': 1
        }
        with self.assertRaises(ArcimotoArgumentError):
            recall_functions.recall_service_vehicle(args)

    def test_recall_remove_vehicle_error_input_vehicle_recall_id_must_be_positive_integer(self):
        with self.assertRaises(ArcimotoArgumentError):
            recall_functions.recall_remove_vehicle({'vehicle_recall_id': -1})

    def test_recall_remove_vehicle_error_input_recall_id_must_be_positive_integer(self):
        args = {
            'recall_id': -1,
            'vins': [self.vin]
        }
        with self.assertRaises(ArcimotoArgumentError):
            recall_functions.recall_remove_vehicle(args)

    def test_recall_service_vehicle_error_user_unauthorized(self):
        with self.assertRaises(ArcimotoPermissionError):
            recall_functions.recall_service_vehicle({}, False)


@arcimoto.runtime.handler
def test_recall_service_vehicle():

    return arcimoto.tests.handle_test_result(unittest.TextTestRunner().run(
        unittest.TestLoader().loadTestsFromTestCase(RecallServiceVehicleTestCase)
    ))


lambda_handler = test_recall_service_vehicle
