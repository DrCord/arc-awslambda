import unittest
import copy

from arcimoto.exceptions import *
import arcimoto.runtime
import arcimoto.tests
import locations_functions


class LocationAccountingLocationCodeSetTestCase(unittest.TestCase):

    location_id = None
    args_a = {
        'location_id': None,
        'accounting_location_code_id': None
    }
    args_b = {
        'location_id': None,
        'accounting_location_code_id': None
    }
    accounting_location_code_id_a = None
    a_args = {
        'code': 'test1'
    }
    b_args = {
        'code': 'test2'
    }
    accounting_location_code_id_b = None

    l_args = {
        'location_name': 'Unit Test Headquarters',
        'street_number': 1234,
        'structure_name': 'Test-Eddifice',
        'street_number_suffix': 'A',
        'street_name': 'Create',
        'street_type': 'Row',
        'street_direction': 'NE',
        'address_type': 1,
        'address_type_identifier': '5678',
        'city': 'Smalltown',
        'governing_district': 'Pennsylvania',
        'postal_area': '12345',
        'local_municipality': 'Village Green',
        'country': 'US',
        'gps_latitude': -123.0054,
        'gps_longitude': 123.0054
    }

    @property
    def location_id_invalid(self):
        list = locations_functions.locations_list().get('locations', None)
        return list[-1].get('id', 0) + 1

    @classmethod
    def setUpClass(cls):
        # location
        cls.location_id = locations_functions.location_create(cls.l_args).get('id', None)
        if cls.location_id is None:
            raise ArcimotoException('Unable to create location for unit tests setup')
        cls.args_a['location_id'] = cls.location_id
        cls.args_b['location_id'] = cls.location_id
        # accounting location code
        response = locations_functions.accounting_location_code_create(cls.a_args)
        cls.accounting_location_code_id = response.get('id', None)
        if cls.accounting_location_code_id is None:
            raise ArcimotoException('Unable to create accounting location code for unit tests setup')
        cls.args_a['accounting_location_code_id'] = cls.accounting_location_code_id
        response = locations_functions.accounting_location_code_create(cls.b_args)
        cls.accounting_location_code_id_b = response.get('id', None)
        if cls.accounting_location_code_id_b is None:
            raise ArcimotoException('Unable to create accounting location code b for unit tests setup')
        cls.args_b['accounting_location_code_id'] = cls.accounting_location_code_id_b

    @classmethod
    def tearDownClass(cls):
        if cls.location_id is not None:
            locations_functions.location_delete(cls.location_id)
        if cls.accounting_location_code_id is not None:
            locations_functions.accounting_location_code_delete({'id': cls.accounting_location_code_id})
        if cls.accounting_location_code_id_b is not None:
            locations_functions.accounting_location_code_delete({'id': cls.accounting_location_code_id_b})

    def test_location_accounting_location_code_set_success(self):
        self.assertIsInstance(locations_functions.location_accounting_location_code_set(self.args_a), dict)

    def test_location_accounting_location_code_reset_success(self):
        """Tests unique column values for location - query will error on constraint if values not reset"""
        self.assertIsInstance(locations_functions.location_accounting_location_code_set(self.args_b), dict)

    # test errors
    def test_location_accounting_location_code_set_error_input_null_vehicle_group_id(self):
        args = copy.deepcopy(self.args_a)
        args['location_id'] = None
        with self.assertRaises(ArcimotoArgumentError):
            locations_functions.location_accounting_location_code_set(args)

    def test_location_accounting_location_code_set_error_input_invalid_type_location_id(self):
        args = copy.deepcopy(self.args_a)
        args['location_id'] = 'not an integer'
        with self.assertRaises(ArcimotoArgumentError):
            locations_functions.location_accounting_location_code_set(args)

    def test_location_accounting_location_code_set_error_input_invalid_type_accounting_location_id(self):
        args = copy.deepcopy(self.args_a)
        args['accounting_location_code_id'] = 'not an integer'
        with self.assertRaises(ArcimotoArgumentError):
            locations_functions.location_accounting_location_code_set(args)

    def test_location_accounting_location_code_set_error_input_invalid_location_id_must_be_positive_integer(self):
        args = copy.deepcopy(self.args_a)
        args['location_id'] = -1
        with self.assertRaises(ArcimotoArgumentError):
            locations_functions.location_accounting_location_code_set(args)

    def test_location_accounting_location_code_set_error_invalid_location_id(self):
        args = copy.deepcopy(self.args_a)
        args['location_id'] = self.location_id_invalid
        with self.assertRaises(ArcimotoNotFoundError):
            locations_functions.location_accounting_location_code_set(args)

    def test_locations_accounting_location_code_set_error_user_unauthorized(self):
        args = copy.deepcopy(self.args_a)
        with self.assertRaises(ArcimotoPermissionError):
            locations_functions.location_accounting_location_code_set(args, False)


@arcimoto.runtime.handler
def test_locations_location_accounting_location_code_set():
    return arcimoto.tests.handle_test_result(unittest.TextTestRunner().run(
        unittest.TestLoader().loadTestsFromTestCase(LocationAccountingLocationCodeSetTestCase)
    ))


lambda_handler = test_locations_location_accounting_location_code_set
