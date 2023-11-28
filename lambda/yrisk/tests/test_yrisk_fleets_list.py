import logging
import unittest
import copy
import uuid

from arcimoto.exceptions import *
import arcimoto.runtime
import arcimoto.tests
import yrisk_functions

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class YriskFleetsListTestCase(unittest.TestCase):

    def test_yrisk_fleets_list_success(self):
        self.assertIsInstance(yrisk_functions.fleets_list(), dict)


@arcimoto.runtime.handler
def test_yrisk_fleets_list():
    return arcimoto.tests.handle_test_result(unittest.TextTestRunner().run(
        unittest.TestLoader().loadTestsFromTestCase(YriskFleetsListTestCase)
    ))


lambda_handler = test_yrisk_fleets_list
