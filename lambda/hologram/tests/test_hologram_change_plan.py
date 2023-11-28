import logging
import unittest
import copy

from arcimoto.exceptions import *
import arcimoto.runtime
import arcimoto.tests

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class HologramChangePlanTestCase(unittest.TestCase):
    '''
    Hologram changes typically can cost money to make as they prorate things in their favor.
    Be careful using this and do not hook it into an automatted workflow without revision.
    '''

    args = {
        'Records': [
            {
                'body': {
                    'device': '495247',  # DEV-KEITHBENCH link id
                    'plan': 204     # 250MB plan default, should already be set to this plan
                    # 'plan': 202     # Professional Plan Flexible Data
                    # 'plan': 205     # Professional Edition 500 MB
                }
            }
        ]
    }

    # unable to test success for vehicles due to hologram not allowing a plan change to the same plan you are on
    # changing plans and back again would cost money by holograms model...

    # test errors
    def test_hologram_change_plan_error_input_null_Records(self):
        with self.assertRaises(ArcimotoArgumentError):
            arcimoto.runtime.invoke_lambda('hologram_change_plan', {'Records': None})

    def test_hologram_change_plan_error_input_invalid_type_Records(self):
        with self.assertRaises(ArcimotoArgumentError):
            arcimoto.runtime.invoke_lambda('hologram_change_plan', {'Records': 'not a list'})

    def test_hologram_change_plan_error_input_invalid_empty_Records(self):
        with self.assertRaises(ArcimotoArgumentError):
            arcimoto.runtime.invoke_lambda('hologram_change_plan', {'Records': []})

    def test_hologram_change_plan_error_input_null_records(self):
        with self.assertRaises(ArcimotoArgumentError):
            arcimoto.runtime.invoke_lambda('hologram_change_plan', {'records': None})

    def test_hologram_change_plan_error_input_invalid_type_records(self):
        with self.assertRaises(ArcimotoArgumentError):
            arcimoto.runtime.invoke_lambda('hologram_change_plan', {'records': 'not a list'})

    def test_hologram_change_plan_error_input_invalid_empty_records(self):
        with self.assertRaises(ArcimotoArgumentError):
            arcimoto.runtime.invoke_lambda('hologram_change_plan', {'records': []})


@arcimoto.runtime.handler
def test_hologram_change_plan():
    return arcimoto.tests.handle_test_result(unittest.TextTestRunner().run(
        unittest.TestLoader().loadTestsFromTestCase(HologramChangePlanTestCase)
    ))


lambda_handler = test_hologram_change_plan
