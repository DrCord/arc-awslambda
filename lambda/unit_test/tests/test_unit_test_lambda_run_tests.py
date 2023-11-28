from copy import deepcopy
import logging
import unittest

from arcimoto.exceptions import *
import arcimoto.runtime
import arcimoto.tests
import unit_test_functions

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class UnitTestLambdaRunTestsTestCase(unittest.TestCase):

    args = {
        'lambda_name': 'unit_test_lambda_get_tests',
        'lambda_tests': [
            'test_unit_test_lambda_get_tests'
        ]
    }

    def test_unit_test_lambda_run_tests_success(self):
        self.assertIsInstance(unit_test_functions.unit_test_lambda_run_tests(self.args), dict)

    # test errors
    def test_unit_test_lambda_run_tests_error_input_no_lambda_name(self):
        args = deepcopy(self.args)
        del args['lambda_name']
        with self.assertRaises(ArcimotoArgumentError):
            unit_test_functions.unit_test_lambda_run_tests(args)

    def test_unit_test_lambda_run_tests_error_input_invalid_type_lambda_name(self):
        args = deepcopy(self.args)
        args['lambda_name'] = 1
        with self.assertRaises(ArcimotoArgumentError):
            unit_test_functions.unit_test_lambda_run_tests(args)

    def test_unit_test_lambda_run_tests_error_input_null_lambda_name(self):
        args = deepcopy(self.args)
        args['lambda_name'] = None
        with self.assertRaises(ArcimotoArgumentError):
            unit_test_functions.unit_test_lambda_run_tests(args)

    def test_unit_test_lambda_run_tests_error_input_empty_lambda_name(self):
        args = deepcopy(self.args)
        args['lambda_name'] = ''
        with self.assertRaises(ArcimotoArgumentError):
            unit_test_functions.unit_test_lambda_run_tests(args)

    def test_unit_test_lambda_run_tests_error_input_empty_lambda_tests(self):
        args = deepcopy(self.args)
        del args['lambda_tests']
        with self.assertRaises(ArcimotoArgumentError):
            unit_test_functions.unit_test_lambda_run_tests(args)

    def test_unit_test_lambda_run_tests_error_input_null_lambda_tests(self):
        args = deepcopy(self.args)
        args['lambda_tests'] = None
        with self.assertRaises(ArcimotoArgumentError):
            unit_test_functions.unit_test_lambda_run_tests(args)

    def test_unit_test_lambda_run_tests_error_input_invalid_type_lambda_tests(self):
        args = deepcopy(self.args)
        args['lambda_tests'] = 'not a list'
        with self.assertRaises(ArcimotoArgumentError):
            unit_test_functions.unit_test_lambda_run_tests(args)


@arcimoto.runtime.handler
def test_unit_test_lambda_run_tests():
    return arcimoto.tests.handle_test_result(unittest.TextTestRunner().run(
        unittest.TestLoader().loadTestsFromTestCase(UnitTestLambdaRunTestsTestCase)
    ))


lambda_handler = test_unit_test_lambda_run_tests
