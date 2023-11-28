import logging
import unittest

from arcimoto.exceptions import *
import arcimoto.runtime
import arcimoto.tests
import userpool_functions

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class UserpoolTriggerCustomMessageTestCase(unittest.TestCase):

    def test_userpool_trigger_custom_message_success(self):
        self.assertIsInstance(userpool_functions.userpool_trigger_custom_message(), dict)


@arcimoto.runtime.handler
def test_userpool_trigger_custom_message():
    return arcimoto.tests.handle_test_result(unittest.TextTestRunner().run(
        unittest.TestLoader().loadTestsFromTestCase(UserpoolTriggerCustomMessageTestCase)
    ))


lambda_handler = test_userpool_trigger_custom_message
