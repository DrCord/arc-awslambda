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


class RecallAddVehicleTestCase(unittest.TestCase):

    args = {
        'recall_id': None,
        'service_reference': None,
        'vins': None
    }
    vin = None
    vin2 = None

    @property
    def recall_id_invalid(self):
        return recall_functions.recalls_get_highest_id() + 1

    @property
    def vin_invalid(self):
        return arcimoto.tests.uuid_vin_get()

    @classmethod
    def setUpClass(cls):
        cls.vin = arcimoto.tests.uuid_vin_get()
        arcimoto.tests.vehicle_create(cls.vin)
        cls.args['vins'] = [cls.vin]

        cls.vin2 = arcimoto.tests.uuid_vin_get()
        arcimoto.tests.vehicle_create(cls.vin2)

        cls.vin3 = arcimoto.tests.uuid_vin_get()
        arcimoto.tests.vehicle_create(cls.vin3)

        cls.vin4 = arcimoto.tests.uuid_vin_get()
        arcimoto.tests.vehicle_create(cls.vin4)

        cls.vin5 = arcimoto.tests.uuid_vin_get()
        arcimoto.tests.vehicle_create(cls.vin5)

        cls.recall_id = recall_functions.recall_create()
        cls.args['recall_id'] = cls.recall_id
        cls.recall_id2 = recall_functions.recall_create()

    @classmethod
    def tearDownClass(cls):
        args = copy.deepcopy(cls.args)
        args['vehicle_recall_id'] = None
        if cls.recall_id is not None:
            recall_functions.recall_remove_vehicle({'recall_id': cls.recall_id, 'vin': cls.vin})
            recall_functions.recall_remove_vehicle({'recall_id': cls.recall_id, 'vin': cls.vin2})
            recall_functions.recall_remove_vehicle({'recall_id': cls.recall_id, 'vin': cls.vin3})
            recall_functions.recall_remove_vehicle({'recall_id': cls.recall_id, 'vin': cls.vin4})
            recall_functions.recall_remove_vehicle({'recall_id': cls.recall_id, 'vin': cls.vin5})
            recall_functions.recall_delete(cls.recall_id)
        if cls.recall_id2 is not None:
            recall_functions.recall_remove_vehicle({'recall_id': cls.recall_id2, 'vin': cls.vin})
            recall_functions.recall_delete(cls.recall_id2)
        arcimoto.tests.vehicle_delete(cls.vin)
        arcimoto.tests.vehicle_delete(cls.vin2)
        arcimoto.tests.vehicle_delete(cls.vin3)
        arcimoto.tests.vehicle_delete(cls.vin4)
        arcimoto.tests.vehicle_delete(cls.vin5)

    def test_recall_add_vehicle_success_single_vin(self):
        args = copy.deepcopy(self.args)
        args['vins'] = [self.vin5]
        self.assertIsInstance(recall_functions.recall_add_vehicle(args), dict)

    def test_recall_add_vehicle_success_multiple_vins(self):
        args = copy.deepcopy(self.args)
        args['vins'] = [self.vin3, self.vin4]
        self.assertIsInstance(recall_functions.recall_add_vehicle(self.args), dict)

    def test_recall_add_vehicle_success_input_service_reference(self):
        args = copy.deepcopy(self.args)
        args['service_reference'] = 'unit_test_service_reference'
        args['vins'] = [self.vin2]
        self.assertIsInstance(recall_functions.recall_add_vehicle(args), dict)

    # test errors
    def test_recall_add_vehicle_error_input_null_recall_id(self):
        args = copy.deepcopy(self.args)
        args['recall_id'] = None
        with self.assertRaises(ArcimotoArgumentError):
            recall_functions.recall_add_vehicle(args)

    def test_recall_add_vehicle_error_input_null_vins(self):
        args = copy.deepcopy(self.args)
        args['vins'] = None
        with self.assertRaises(ArcimotoArgumentError):
            recall_functions.recall_add_vehicle(args)

    def test_recall_add_vehicle_error_input_empty_vins(self):
        args = copy.deepcopy(self.args)
        args['vins'] = []
        with self.assertRaises(ArcimotoArgumentError):
            recall_functions.recall_add_vehicle(args)

    def test_recall_add_vehicle_error_input_invalid_recall_id_must_be_positive_integer(self):
        args = copy.deepcopy(self.args)
        args['recall_id'] = -1
        with self.assertRaises(ArcimotoArgumentError):
            recall_functions.recall_add_vehicle(args)

    def test_recall_add_vehicle_error_input_invalid_type_recall_id(self):
        args = copy.deepcopy(self.args)
        args['recall_id'] = 'not an integer'
        with self.assertRaises(ArcimotoArgumentError):
            recall_functions.recall_add_vehicle(args)

    def test_recall_add_vehicle_error_input_invalid_recall_id(self):
        args = copy.deepcopy(self.args)
        args['recall_id'] = self.recall_id_invalid
        with self.assertRaises(ArcimotoArgumentError):
            recall_functions.recall_add_vehicle(args)

    def test_recall_add_vehicle_error_invalid_vin(self):
        args = copy.deepcopy(self.args)
        vin_invalid = self.vin_invalid
        args['vins'] = [vin_invalid]
        with self.assertRaises(ArcimotoArgumentError):
            recall_functions.recall_add_vehicle(args)

    def test_recall_add_vehicle_error_invalid_vins(self):
        args = copy.deepcopy(self.args)
        vin_invalid1 = self.vin_invalid
        vin_invalid2 = self.vin_invalid
        args['vins'] = [vin_invalid1, vin_invalid2]
        with self.assertRaises(ArcimotoArgumentError):
            recall_functions.recall_add_vehicle(args)

    def test_recall_add_vehicle_error_input_invalid_type_vins(self):
        args = copy.deepcopy(self.args)
        args['vins'] = 'not a list'
        with self.assertRaises(ArcimotoArgumentError):
            recall_functions.recall_add_vehicle(args)

    def test_recall_add_vehicle_error_input_invalid_type_service_reference(self):
        args = copy.deepcopy(self.args)
        args['service_reference'] = 1
        with self.assertRaises(ArcimotoArgumentError):
            recall_functions.recall_add_vehicle(args)

    def test_recall_add_vehicle_error_vehicle_already_attached_to_recall(self):
        args = copy.deepcopy(self.args)
        args['recall_id'] = self.recall_id2
        recall_functions.recall_add_vehicle(args)
        with self.assertRaises(ArcimotoArgumentError):
            recall_functions.recall_add_vehicle(args)
        args['vehicle_recall_id'] = None
        recall_functions.recall_remove_vehicle({'recall_id': self.recall_id2, 'vin': self.vin})

    def test_recall_add_vehicle_error_user_unauthorized(self):
        args = copy.deepcopy(self.args)
        with self.assertRaises(ArcimotoPermissionError):
            recall_functions.recall_add_vehicle(args, False)


@arcimoto.runtime.handler
def test_recall_add_vehicle():
    return arcimoto.tests.handle_test_result(unittest.TextTestRunner().run(
        unittest.TestLoader().loadTestsFromTestCase(RecallAddVehicleTestCase)
    ))


lambda_handler = test_recall_add_vehicle
