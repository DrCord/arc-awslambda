import logging
import unittest

from arcimoto.exceptions import *
import arcimoto.runtime
import arcimoto.tests
import reef_functions

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class ReefManagedSessionListTestCase(unittest.TestCase):

    def test_reef_managed_session_list_success(self):
        self.assertIsInstance(reef_functions.managed_session_list(), dict)


@arcimoto.runtime.handler
def test_reef_managed_session_list():
    return arcimoto.tests.handle_test_result(unittest.TextTestRunner().run(
        unittest.TestLoader().loadTestsFromTestCase(ReefManagedSessionListTestCase)
    ))


lambda_handler = test_reef_managed_session_list
