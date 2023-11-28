import logging
import unittest

from arcimoto.exceptions import *
import arcimoto.runtime
import arcimoto.tests
import unit_test_functions

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class UnitTestLambdaGetTestsTestCase(unittest.TestCase):

    args = {
        'lambda_name': 'unit_test_lambda_bundles_get_lambdas'
    }

    def test_unit_test_lambda_get_tests_success(self):
        self.assertIsInstance(unit_test_functions.unit_test_lambda_get_tests(self.args), dict)

    # test errors
    def test_unit_test_lambda_get_tests_error_input_no_lambda_name(self):
        with self.assertRaises(ArcimotoArgumentError):
            unit_test_functions.unit_test_lambda_get_tests({})

    def test_unit_test_lambda_get_tests_error_input_invalid_type_lambda_name(self):
        with self.assertRaises(ArcimotoArgumentError):
            unit_test_functions.unit_test_lambda_get_tests({'lambda_name': 1})

    def test_unit_test_lambda_get_tests_error_input_null_lambda_name(self):
        with self.assertRaises(ArcimotoArgumentError):
            unit_test_functions.unit_test_lambda_get_tests({'lambda_name': None})

    def test_unit_test_lambda_get_tests_error_input_empty_lambda_name(self):
        with self.assertRaises(ArcimotoArgumentError):
            unit_test_functions.unit_test_lambda_get_tests({'lambda_name': ''})


@arcimoto.runtime.handler
def test_unit_test_lambda_get_tests():
    return arcimoto.tests.handle_test_result(unittest.TextTestRunner().run(
        unittest.TestLoader().loadTestsFromTestCase(UnitTestLambdaGetTestsTestCase)
    ))


lambda_handler = test_unit_test_lambda_get_tests
