import logging
import unittest

from arcimoto.exceptions import *
import arcimoto.runtime
import arcimoto.tests
import yrisk_functions

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class YriskNotifyEmailTestCase(unittest.TestCase):

    def test_yrisk_notify_email_success(self):
        self.assertIsInstance(yrisk_functions.notify_email(), dict)


@arcimoto.runtime.handler
def test_yrisk_notify_email():
    return arcimoto.tests.handle_test_result(unittest.TextTestRunner().run(
        unittest.TestLoader().loadTestsFromTestCase(YriskNotifyEmailTestCase)
    ))


lambda_handler = test_yrisk_notify_email
