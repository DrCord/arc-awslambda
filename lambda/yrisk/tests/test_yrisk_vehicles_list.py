import logging
import unittest
import copy
import uuid

from arcimoto.exceptions import *
import arcimoto.runtime
import arcimoto.tests
import fleets_functions
import yrisk_functions

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class YriskVehiclesListTestCase(unittest.TestCase):

    args = {
        'fleets_db_data': {
            'vehicle_groups': [1]
        }
    }

    def test_yrisk_vehicles_list_success(self):
        self.assertIsInstance(yrisk_functions.vehicles_list(self.args), dict)


@arcimoto.runtime.handler
def test_yrisk_vehicles_list():
    return arcimoto.tests.handle_test_result(unittest.TextTestRunner().run(
        unittest.TestLoader().loadTestsFromTestCase(YriskVehiclesListTestCase)
    ))


lambda_handler = test_yrisk_vehicles_list
