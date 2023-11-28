import logging
import unittest

from arcimoto.exceptions import *
import arcimoto.runtime
import arcimoto.tests
import managed_session_functions

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class ManagedSessionListTestCase(unittest.TestCase):

    def test_managed_session_list_success(self):
        self.assertIsInstance(managed_session_functions.list(), dict)

    # test errors
    def test_managed_session_list_error_unauthorized(self):
        with self.assertRaises(ArcimotoPermissionError):
            managed_session_functions.list(False)


@arcimoto.runtime.handler
def test_managed_session_list():
    return arcimoto.tests.handle_test_result(unittest.TextTestRunner().run(
        unittest.TestLoader().loadTestsFromTestCase(ManagedSessionListTestCase)
    ))


lambda_handler = test_managed_session_list
