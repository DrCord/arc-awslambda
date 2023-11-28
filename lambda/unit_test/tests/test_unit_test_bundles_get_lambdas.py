from copy import deepcopy
import logging
import unittest

from arcimoto.exceptions import *
import arcimoto.runtime
import arcimoto.tests
import unit_test_functions

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class UnitTestBundlesGetLambdasTestCase(unittest.TestCase):

    args = {
        'bundles': [
            'alarms',
            'authorities',
            'backfill',
            'debug',
            'firmware',
            'fleets',
            'grafana',
            'hologram',
            'locations',
            'managed_session',
            'notes',
            'orders',
            'recalls',
            'reef',
            'replicate',
            'sheer_id',
            'telemetry',
            'tests',
            'userpool',
            'users',
            'utility',
            'vehicles',
            'yrisk'
        ]
    }

    def test_unit_test_bundles_get_lambdas_success_not_empty_bundles(self):
        self.assertIsInstance(unit_test_functions.unit_test_bundles_get_lambdas(self.args), dict)

    def test_unit_test_bundles_get_lambdas_success_empty_bundles(self):
        args = deepcopy(self.args)
        args['bundles'] = []
        self.assertIsInstance(unit_test_functions.unit_test_bundles_get_lambdas(args), dict)

    # test errors
    def test_unit_test_bundles_get_lambdas_error_input_invalid_type_bundles(self):
        args = deepcopy(self.args)
        args['bundles'] = 'not a list'
        with self.assertRaises(ArcimotoArgumentError):
            unit_test_functions.unit_test_bundles_get_lambdas(args)


@arcimoto.runtime.handler
def test_unit_test_bundles_get_lambdas():
    return arcimoto.tests.handle_test_result(unittest.TextTestRunner().run(
        unittest.TestLoader().loadTestsFromTestCase(UnitTestBundlesGetLambdasTestCase)
    ))


lambda_handler = test_unit_test_bundles_get_lambdas
