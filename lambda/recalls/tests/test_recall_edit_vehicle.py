import logging
import unittest
import copy
from datetime import datetime

from arcimoto.exceptions import *
import arcimoto.runtime
import arcimoto.tests
import recall_functions

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class RecallEditVehicleTestCase(unittest.TestCase):

    args = {
        'id': None,
        'recall_id': None,
        'service_date': None,
        'service_reference': 'Edited by unit test',
        'vin': None
    }

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
        cls.timestamp = str(datetime.utcnow())
        cls.test_vin = arcimoto.tests.uuid_vin_get()
        cls.test_vin2 = arcimoto.tests.uuid_vin_get()
        arcimoto.tests.vehicle_create(cls.test_vin)
        arcimoto.tests.vehicle_create(cls.test_vin2)
        cls.recall_id = recall_functions.recall_create()
        args = {
            'recall_id': cls.recall_id,
            'vins': [cls.test_vin]
        }
        cls.vehicle_recall_1 = recall_functions.recall_add_vehicle(args)
        cls.vehicle_recall_id1 = cls.vehicle_recall_1.get('vehicle_recall_ids')[0]
        args['vins'] = [cls.test_vin2]
        cls.vehicle_recall_2 = recall_functions.recall_add_vehicle(args)
        cls.vehicle_recall_id2 = cls.vehicle_recall_2.get('vehicle_recall_ids')[0]

    @classmethod
    def tearDownClass(cls):
        arcimoto.tests.vehicle_delete(cls.test_vin)
        arcimoto.tests.vehicle_delete(cls.test_vin2)
        if cls.recall_id is not None:
            recall_functions.recall_delete(cls.recall_id)

    def test_recall_edit_vehicle_success_input_id(self):
        args = copy.deepcopy(self.args)
        args['id'] = self.vehicle_recall_id1
        vehicle_recall = recall_functions.recall_edit_vehicle(args)
        self.assertTrue(vehicle_recall.get('service_reference', None) == args['service_reference'])

    def test_recall_edit_vehicle_success_input_recall_id_and_vin(self):
        args = copy.deepcopy(self.args)
        args['recall_id'] = self.recall_id
        args['vin'] = self.test_vin
        vehicle_recall = recall_functions.recall_edit_vehicle(args)
        self.assertTrue(vehicle_recall.get('service_reference', None) == args['service_reference'])

    def test_recall_edit_vehicle_success_input_id_and_service_date(self):
        args = copy.deepcopy(self.args)
        args['id'] = self.vehicle_recall_id1
        args['service_reference'] = None
        args['service_date'] = self.timestamp
        self.assertIsInstance(recall_functions.recall_edit_vehicle(args), dict)

    def test_recall_edit_vehicle_success_input_id_and_service_reference_and_service_date(self):
        args = copy.deepcopy(self.args)
        args['id'] = self.vehicle_recall_id1
        args['service_date'] = self.timestamp
        self.assertIsInstance(recall_functions.recall_edit_vehicle(args), dict)

    # test errors
    def test_recall_edit_vehicle_error_input_null_id(self):
        args = copy.deepcopy(self.args)
        with self.assertRaises(ArcimotoArgumentError):
            recall_functions.recall_edit_vehicle(args)

    def test_recall_edit_vehicle_error_input_recall_id_and_vin_not_used_together(self):
        args = copy.deepcopy(self.args)
        args['vin'] = self.test_vin
        with self.assertRaises(ArcimotoArgumentError):
            recall_functions.recall_edit_vehicle(args)
        args['recall_id'] = self.recall_id
        args['vin'] = None
        with self.assertRaises(ArcimotoArgumentError):
            recall_functions.recall_edit_vehicle(args)

    def test_recall_edit_vehicle_error_input_no_edits(self):
        args = copy.deepcopy(self.args)
        args['id'] = self.vehicle_recall_id1
        args['service_reference'] = None
        with self.assertRaises(ArcimotoArgumentError):
            recall_functions.recall_edit_vehicle(args)

    def test_recall_edit_vehicle_error_invalid_id_must_be_positive_integer(self):
        args = copy.deepcopy(self.args)
        args['id'] = -1
        with self.assertRaises(ArcimotoArgumentError):
            recall_functions.recall_edit_vehicle(args)

    def test_recall_edit_vehicle_error_invalid_recall_id_must_be_positive_integer(self):
        args = copy.deepcopy(self.args)
        args['recall_id'] = -1
        args['vin'] = self.test_vin
        with self.assertRaises(ArcimotoArgumentError):
            recall_functions.recall_edit_vehicle(args)

    def test_recall_edit_vehicle_error_invalid_id_does_not_exist_in_vehicle_recalls_table(self):
        args = copy.deepcopy(self.args)
        args['id'] = self.vehicle_recall_id_invalid
        with self.assertRaises(ArcimotoArgumentError):
            recall_functions.recall_edit_vehicle(args)

    def test_recall_edit_vehicle_error_invalid_recall_id_does_not_exist_in_recalls_table(self):
        args = copy.deepcopy(self.args)
        args['recall_id'] = self.recall_id_invalid
        args['vin'] = self.test_vin
        with self.assertRaises(ArcimotoArgumentError):
            recall_functions.recall_edit_vehicle(args)

    def test_recall_edit_vehicle_error_invalid_vin(self):
        args = copy.deepcopy(self.args)
        args['recall_id'] = self.recall_id
        args['vin'] = self.vin_invalid
        with self.assertRaises(ArcimotoArgumentError):
            recall_functions.recall_edit_vehicle(args)

    def test_recall_edit_vehicle_error_vin_already_exists_in_vehicle_recalls_table_for_recall(self):
        args = copy.deepcopy(self.args)
        args['id'] = self.vehicle_recall_id2
        args['vin'] = self.test_vin
        with self.assertRaises(ArcimotoArgumentError):
            recall_functions.recall_edit_vehicle(args)

    def test_recall_edit_vehicle_error_input_invalid_type_id(self):
        args = copy.deepcopy(self.args)
        args['id'] = 'not an integer'
        with self.assertRaises(ArcimotoArgumentError):
            recall_functions.recall_edit_vehicle(args)

    def test_recall_edit_vehicle_error_input_invalid_type_recall_id(self):
        args = copy.deepcopy(self.args)
        args['recall_id'] = 'not an integer'
        args['vin'] = self.test_vin
        with self.assertRaises(ArcimotoArgumentError):
            recall_functions.recall_edit_vehicle(args)

    def test_recall_edit_vehicle_error_input_invalid_type_vin(self):
        args = copy.deepcopy(self.args)
        args['recall_id'] = self.recall_id
        args['vin'] = 1
        with self.assertRaises(ArcimotoArgumentError):
            recall_functions.recall_edit_vehicle(args)

    def test_recall_edit_vehicle_error_user_unauthorized(self):
        args = copy.deepcopy(self.args)
        args['id'] = self.vehicle_recall_id1
        with self.assertRaises(ArcimotoPermissionError):
            recall_functions.recall_edit_vehicle(args, False)


@arcimoto.runtime.handler
def test_recall_edit_vehicle():
    return arcimoto.tests.handle_test_result(unittest.TextTestRunner().run(
        unittest.TestLoader().loadTestsFromTestCase(RecallEditVehicleTestCase)
    ))


lambda_handler = test_recall_edit_vehicle
