import unittest
import copy

from arcimoto.exceptions import *
import arcimoto.runtime
import arcimoto.tests
import fleets_functions


class VehicleGroupAccountingDepartmentCodeSetTestCase(unittest.TestCase):

    vehicle_group_id = None
    vehicle_code_args = {
        'vehicle_group_id': None,
        'accounting_department_code_id': None
    }
    vehicle_code_reset_args = {
        'vehicle_group_id': None,
        'accounting_department_code_id': None
    }
    dept_code_args = {
        'code': 'test_1',
        'description': 'test description'
    }
    dept_code_reset_args = {
        'code': 'test_2',
        'description': 'test description'
    }
    accounting_department_code_id = None
    accounting_department_code_reset_id = None

    @property
    def group_id_invalid(self):
        return fleets_functions.vehicle_groups_list()[-1].get('id', 0) + 1

    @classmethod
    def setUpClass(cls):
        # vehicle group
        cls.vehicle_group_id = fleets_functions.vehicle_group_create()
        if cls.vehicle_group_id is None:
            raise ArcimotoException('Unable to create vehicle group for unit tests setup')
        cls.vehicle_code_args['vehicle_group_id'] = cls.vehicle_group_id
        cls.vehicle_code_reset_args['vehicle_group_id'] = cls.vehicle_group_id
        # accounting department code
        response = fleets_functions.accounting_department_code_create(cls.dept_code_args)
        cls.accounting_department_code_id = response.get('id', None)
        if cls.accounting_department_code_id is None:
            raise ArcimotoException('Unable to create accounting_department_code_a for unit tests setup')
        cls.vehicle_code_args['accounting_department_code_id'] = cls.accounting_department_code_id
        response = fleets_functions.accounting_department_code_create(cls.dept_code_reset_args)
        cls.accounting_department_code_reset_id = response.get('id', None)
        if cls.accounting_department_code_reset_id is None:
            raise ArcimotoException('Unable to create accounting_department_code_b for unit tests setup')
        cls.vehicle_code_reset_args['accounting_department_code_id'] = cls.accounting_department_code_reset_id

    @classmethod
    def tearDownClass(cls):
        if cls.vehicle_group_id is not None:
            fleets_functions.vehicle_group_delete(cls.vehicle_group_id)
        if cls.accounting_department_code_id is not None:
            fleets_functions.accounting_department_code_delete({'id': cls.accounting_department_code_id})
        if cls.accounting_department_code_reset_id is not None:
            fleets_functions.accounting_department_code_delete({'id': cls.accounting_department_code_reset_id})

    def test_vehicle_group_accounting_department_code_set_success(self):
        self.assertIsInstance(fleets_functions.vehicle_group_accounting_department_code_set(self.vehicle_code_args), dict)

    def test_vehicle_group_accounting_department_code_reset_success(self):
        self.assertIsInstance(fleets_functions.vehicle_group_accounting_department_code_set(self.vehicle_code_reset_args), dict)

    # test errors
    def test_vehicle_group_accounting_department_code_set_error_input_null_vehicle_group_id(self):
        args = copy.deepcopy(self.vehicle_code_args)
        args['vehicle_group_id'] = None
        with self.assertRaises(ArcimotoArgumentError):
            fleets_functions.vehicle_group_accounting_department_code_set(args)

    def test_vehicle_group_accounting_department_code_set_error_input_invalid_type_vehicle_group_id(self):
        args = copy.deepcopy(self.vehicle_code_args)
        args['vehicle_group_id'] = 'not an integer'
        with self.assertRaises(ArcimotoArgumentError):
            fleets_functions.vehicle_group_accounting_department_code_set(args)

    def test_vehicle_group_accounting_department_code_set_error_input_invalid_type_accounting_code_id(self):
        args = copy.deepcopy(self.vehicle_code_args)
        args['accounting_department_code_id'] = 'not an integer'
        with self.assertRaises(ArcimotoArgumentError):
            fleets_functions.vehicle_group_accounting_department_code_set(args)

    def test_vehicle_group_accounting_department_code_set_error_input_invalid_vehicle_group_id_must_be_positive_integer(self):
        args = copy.deepcopy(self.vehicle_code_args)
        args['vehicle_group_id'] = -1
        with self.assertRaises(ArcimotoArgumentError):
            fleets_functions.vehicle_group_accounting_department_code_set(args)

    def test_vehicle_group_accounting_department_code_set_error_invalid_vehicle_group_id(self):
        args = copy.deepcopy(self.vehicle_code_args)
        args['vehicle_group_id'] = self.group_id_invalid
        with self.assertRaises(ArcimotoNotFoundError):
            fleets_functions.vehicle_group_accounting_department_code_set(args)

    def test_vehicle_group_accounting_department_code_set_error_user_unauthorized(self):
        args = copy.deepcopy(self.vehicle_code_args)
        with self.assertRaises(ArcimotoPermissionError):
            fleets_functions.vehicle_group_accounting_department_code_set(args, False)


@arcimoto.runtime.handler
def test_fleets_vehicle_group_accounting_department_code_set():
    return arcimoto.tests.handle_test_result(unittest.TextTestRunner().run(
        unittest.TestLoader().loadTestsFromTestCase(VehicleGroupAccountingDepartmentCodeSetTestCase)
    ))


lambda_handler = test_fleets_vehicle_group_accounting_department_code_set
