import logging
import unittest

from arcimoto.exceptions import *
import arcimoto.runtime
import arcimoto.tests

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class HologramCheckPlansTestCase(unittest.TestCase):
    '''
    Hologram changes typically can cost money to make as they prorate things in their favor.
    Be careful using this and do not hook it into an automatted workflow without revision.
    '''

    def test_hologram_check_plans_success(self):
        self.assertIsInstance(arcimoto.runtime.invoke_lambda('hologram_check_plans', {}), dict)


@arcimoto.runtime.handler
def test_hologram_check_plans():
    return arcimoto.tests.handle_test_result(unittest.TextTestRunner().run(
        unittest.TestLoader().loadTestsFromTestCase(HologramCheckPlansTestCase)
    ))


lambda_handler = test_hologram_check_plans
