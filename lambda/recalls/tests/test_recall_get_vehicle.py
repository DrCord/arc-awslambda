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


class RecallGetVehicleTestCase(unittest.TestCase):

    args = {
        'id': None,
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
        cls.vin = arcimoto.tests.uuid_vin_get()
        arcimoto.tests.vehicle_create(cls.vin)
        cls.recall_id = recall_functions.recall_create()
        cls.args_add_vehicle = {
            'recall_id': cls.recall_id,
            'vins': [cls.vin]
        }
        cls.args_remove_vehicle = {
            'recall_id': cls.recall_id,
            'vin': cls.vin
        }
        cls.vehicle_recall = recall_functions.recall_add_vehicle(cls.args_add_vehicle)
        cls.vehicle_recall_id = cls.vehicle_recall.get('vehicle_recall_ids')[0]

    @classmethod
    def tearDownClass(cls):
        if cls.recall_id is not None:
            args = copy.deepcopy(cls.args_remove_vehicle)
            args['vehicle_recall_id'] = None
            recall_functions.recall_remove_vehicle(args)
            recall_functions.recall_delete(cls.recall_id)
        arcimoto.tests.vehicle_delete(cls.vin)

    def test_recall_get_vehicle_success_input_vehicle_recall_id(self):
        args = copy.deepcopy(self.args)
        args['id'] = self.vehicle_recall_id
        self.assertIsInstance(recall_functions.recall_get_vehicle(args), dict)

    def test_recall_get_vehicle_success_input_recall_id_and_vin(self):
        args = copy.deepcopy(self.args)
        args['recall_id'] = self.recall_id
        args['vin'] = self.vin
        self.assertIsInstance(recall_functions.recall_get_vehicle(args), dict)

    # test errors
    def test_recall_get_vehicle_error_input_recall_id_and_vin_are_required_together(self):
        args = copy.deepcopy(self.args)
        with self.assertRaises(ArcimotoArgumentError):
            args['vin'] = self.vin
            recall_functions.recall_get_vehicle(args)
        with self.assertRaises(ArcimotoArgumentError):
            args['vin'] = self.recall_id
            args['vin'] = None
            recall_functions.recall_get_vehicle(args)

    def test_recall_get_vehicle_error_input_id_must_be_positive_integer(self):
        args = copy.deepcopy(self.args)
        args['id'] = -1
        with self.assertRaises(ArcimotoArgumentError):
            recall_functions.recall_get_vehicle(args)

    def test_recall_get_vehicle_error_input_recall_id_must_be_positive_integer(self):
        args = copy.deepcopy(self.args)
        args['recall_id'] = -1
        args['vin'] = self.vin
        with self.assertRaises(ArcimotoArgumentError):
            recall_functions.recall_get_vehicle(args)

    def test_recall_get_vehicle_error_invalid_id(self):
        args = copy.deepcopy(self.args)
        args['id'] = self.vehicle_recall_id_invalid
        with self.assertRaises(ArcimotoNotFoundError):
            recall_functions.recall_get_vehicle(args)

    def test_recall_get_vehicle_error_invalid_recall_id_and_vin_combination(self):
        args = copy.deepcopy(self.args)
        with self.assertRaises(ArcimotoNotFoundError):
            args['recall_id'] = self.recall_id_invalid
            args['vin'] = self.vin
            recall_functions.recall_get_vehicle(args)
        with self.assertRaises(ArcimotoNotFoundError):
            args['recall_id'] = self.recall_id
            args['vin'] = self.vin_invalid
            recall_functions.recall_get_vehicle(args)

    def test_recall_get_vehicle_error_input_invalid_type_id(self):
        args = copy.deepcopy(self.args)
        args['id'] = 'not an integer'
        with self.assertRaises(ArcimotoArgumentError):
            recall_functions.recall_get_vehicle(args)

    def test_recall_get_vehicle_error_input_invalid_type_recall_id(self):
        args = copy.deepcopy(self.args)
        args['recall_id'] = 'not an integer'
        args['vin'] = self.vin
        with self.assertRaises(ArcimotoArgumentError):
            recall_functions.recall_get_vehicle(args)

    def test_recall_get_vehicle_error_input_invalid_type_vin(self):
        args = copy.deepcopy(self.args)
        args['recall_id'] = self.recall_id
        args['vin'] = 1
        with self.assertRaises(ArcimotoArgumentError):
            recall_functions.recall_get_vehicle(args)

    def test_recall_get_vehicle_error_user_unauthorized(self):
        args = copy.deepcopy(self.args)
        args['id'] = self.vehicle_recall_id
        with self.assertRaises(ArcimotoPermissionError):
            recall_functions.recall_get_vehicle(args, False)


@arcimoto.runtime.handler
def test_recall_get_vehicle():

    return arcimoto.tests.handle_test_result(unittest.TextTestRunner().run(
        unittest.TestLoader().loadTestsFromTestCase(RecallGetVehicleTestCase)
    ))


lambda_handler = test_recall_get_vehicle
