import logging
import unittest
import copy
import json

from arcimoto.exceptions import *
import arcimoto.runtime
import arcimoto.tests

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class UpdateHologramTestCase(unittest.TestCase):
    '''
    Hologram changes typically can cost money to make as they prorate things in their favor.
    Be careful using this and do not hook it into an automatted workflow without revision.
    '''

    vin = arcimoto.tests.uuid_vin_get()
    args = {
        'Records': [
            {
                'body': {
                    'vin': 'DEV-NOT-RYANJ',
                    'data': {
                        'iccid': '8944501810180182922'
                    }
                }
            }
        ]
    }
    args['Records'][0]['body'] = json.dumps(args['Records'][0]['body'])

    def test_update_hologram_success(self):
        args = copy.deepcopy(self.args)
        self.assertIsInstance(arcimoto.runtime.invoke_lambda('update_hologram', args), dict)

    # def test_update_hologram_success_records(self):
    #     args = {}
    #     args['records'] = copy.deepcopy(self.args['Records'])
    #     self.assertIsInstance(arcimoto.runtime.invoke_lambda('update_hologram', args), dict)

    # # test errors
    # def test_update_hologram_error_input_null_Records(self):
    #     with self.assertRaises(ArcimotoArgumentError):
    #         arcimoto.runtime.invoke_lambda('update_hologram', {'Records': None})

    # def test_update_hologram_error_input_invalid_type_Records(self):
    #     with self.assertRaises(ArcimotoArgumentError):
    #         arcimoto.runtime.invoke_lambda('update_hologram', {'Records': 'not a list'})

    # def test_update_hologram_error_input_invalid_empty_Records(self):
    #     with self.assertRaises(ArcimotoArgumentError):
    #         arcimoto.runtime.invoke_lambda('update_hologram', {'Records': []})

    # def test_update_hologram_error_input_null_records(self):
    #     with self.assertRaises(ArcimotoArgumentError):
    #         arcimoto.runtime.invoke_lambda('update_hologram', {'records': None})

    # def test_update_hologram_error_input_invalid_type_records(self):
    #     with self.assertRaises(ArcimotoArgumentError):
    #         arcimoto.runtime.invoke_lambda('update_hologram', {'records': 'not a list'})

    # def test_update_hologram_error_input_invalid_empty_records(self):
    #     with self.assertRaises(ArcimotoArgumentError):
    #         arcimoto.runtime.invoke_lambda('update_hologram', {'records': []})


@arcimoto.runtime.handler
def test_update_hologram():
    return arcimoto.tests.handle_test_result(unittest.TextTestRunner().run(
        unittest.TestLoader().loadTestsFromTestCase(UpdateHologramTestCase)
    ))


lambda_handler = test_update_hologram
