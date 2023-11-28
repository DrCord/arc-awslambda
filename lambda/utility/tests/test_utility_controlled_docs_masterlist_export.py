import logging
import unittest

from arcimoto.exceptions import *
import arcimoto.runtime
import arcimoto.tests
import utility_functions

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class UtilityControlledDocsMasterlistExportTestCase(unittest.TestCase):

    def test_utility_controlled_docs_masterlist_export(self):
        self.assertIsInstance(utility_functions.controlled_docs_masterlist_export(), dict)


@arcimoto.runtime.handler
def test_utility_controlled_docs_masterlist_export():
    return arcimoto.tests.handle_test_result(unittest.TextTestRunner().run(
        unittest.TestLoader().loadTestsFromTestCase(UtilityControlledDocsMasterlistExportTestCase)
    ))


lambda_handler = test_utility_controlled_docs_masterlist_export
