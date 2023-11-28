import logging
import unittest

from arcimoto.exceptions import *
import arcimoto.runtime
import arcimoto.tests
import utility_functions

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class UtilityCwlSetRetentionTestCase(unittest.TestCase):

    def test_utility_cwl_set_retention_success(self):
        self.assertIsInstance(utility_functions.cwl_set_retention(), dict)


@arcimoto.runtime.handler
def test_utility_cwl_set_retention():
    return arcimoto.tests.handle_test_result(unittest.TextTestRunner().run(
        unittest.TestLoader().loadTestsFromTestCase(UtilityCwlSetRetentionTestCase)
    ))


lambda_handler = test_utility_cwl_set_retention
