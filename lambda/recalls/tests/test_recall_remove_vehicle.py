import logging
import unittest
import copy

from arcimoto.exceptions import *
import arcimoto.runtime
import arcimoto.tests
import recall_functions

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class RecallRemoveVehicleTestCase(unittest.TestCase):

    args = {
        'vehicle_recall_id': None,
        'recall_id': None,
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
        if cls.recall_id is not None:
            recall_functions.recall_delete(cls.recall_id)
        arcimoto.tests.vehicle_delete(cls.test_vin)
        arcimoto.tests.vehicle_delete(cls.test_vin2)

    def test_recall_remove_vehicle_success_input_vehicle_recall_id(self):
        args = copy.deepcopy(self.args)
        args['vehicle_recall_id'] = self.vehicle_recall_id1
        recall_functions.recall_remove_vehicle(args)
        recall_vehicles = recall_functions.recall_get(self.recall_id, True).get('vehicles', None)
        self.assertFalse(next((item for item in recall_vehicles if item['vin'] == self.test_vin), None))

    def test_recall_remove_vehicle_success_input_recall_id_and_vin(self):
        args = copy.deepcopy(self.args)
        args['recall_id'] = self.recall_id
        args['vin'] = self.test_vin2
        recall_functions.recall_remove_vehicle(args)
        recall_vehicles = recall_functions.recall_get(self.recall_id, True).get('vehicles', None)
        self.assertFalse(next((item for item in recall_vehicles if item['vin'] == self.test_vin2), None))

    # test errors
    def test_recall_remove_vehicle_error_input_recall_id_and_vin_are_required_together(self):
        args = copy.deepcopy(self.args)
        with self.assertRaises(ArcimotoArgumentError):
            args['vin'] = self.test_vin
            recall_functions.recall_remove_vehicle(args)
        with self.assertRaises(ArcimotoArgumentError):
            args['vin'] = None
            args['recall_id'] = self.recall_id
            recall_functions.recall_remove_vehicle(args)

    def test_recall_remove_vehicle_error_input_vehicle_recall_id_must_be_positive_integer(self):
        args = copy.deepcopy(self.args)
        args['vehicle_recall_id'] = -1
        with self.assertRaises(ArcimotoArgumentError):
            recall_functions.recall_remove_vehicle(args)

    def test_recall_remove_vehicle_error_input_recall_id_must_be_positive_integer(self):
        args = copy.deepcopy(self.args)
        args['recall_id'] = -1
        args['vin'] = self.test_vin
        with self.assertRaises(ArcimotoArgumentError):
            recall_functions.recall_remove_vehicle(args)

    def test_recall_remove_vehicle_error_vehicle_recall_id_does_not_exist_in_vehicle_recalls_table(self):
        args = copy.deepcopy(self.args)
        args['vehicle_recall_id'] = self.vehicle_recall_id_invalid
        with self.assertRaises(ArcimotoArgumentError):
            recall_functions.recall_remove_vehicle(args)

    def test_recall_remove_vehicle_error_recall_id_does_not_exist_in_recalls_table(self):
        args = copy.deepcopy(self.args)
        args['recall_id'] = self.recall_id_invalid
        args['vin'] = self.test_vin
        with self.assertRaises(ArcimotoArgumentError):
            recall_functions.recall_remove_vehicle(args)

    def test_recall_remove_vehicle_error_vin_does_not_exist_in_vehicle_table(self):
        args = copy.deepcopy(self.args)
        args['recall_id'] = self.recall_id
        args['vin'] = self.vin_invalid
        with self.assertRaises(ArcimotoArgumentError):
            recall_functions.recall_remove_vehicle(args)

    def test_recall_remove_vehicle_error_input_invalid_type_vehicle_recall_id(self):
        args = copy.deepcopy(self.args)
        args['vehicle_recall_id'] = 'not an integer'
        with self.assertRaises(ArcimotoArgumentError):
            recall_functions.recall_remove_vehicle(args)

    def test_recall_remove_vehicle_error_input_invalid_type_recall_id(self):
        args = copy.deepcopy(self.args)
        args['recall_id'] = 'not an integer'
        args['vin'] = self.test_vin
        with self.assertRaises(ArcimotoArgumentError):
            recall_functions.recall_remove_vehicle(args)

    def test_recall_remove_vehicle_error_input_invalid_type_vin(self):
        args = copy.deepcopy(self.args)
        args['recall_id'] = self.recall_id
        args['vin'] = 1
        with self.assertRaises(ArcimotoArgumentError):
            recall_functions.recall_remove_vehicle(args)

    def test_recall_remove_vehicle_error_user_unauthorized(self):
        with self.assertRaises(ArcimotoPermissionError):
            recall_functions.recall_remove_vehicle({}, False)


@arcimoto.runtime.handler
def test_recall_remove_vehicle():

    return arcimoto.tests.handle_test_result(unittest.TextTestRunner().run(
        unittest.TestLoader().loadTestsFromTestCase(RecallRemoveVehicleTestCase)
    ))


lambda_handler = test_recall_remove_vehicle
