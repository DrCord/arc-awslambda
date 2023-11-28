import unittest

from arcimoto.exceptions import *
import arcimoto.runtime
import arcimoto.tests
import orders_functions


class OrdersOrderCrmUpdateTestCase(unittest.TestCase):
    """
    Important Note: Order form should be validated at Order Create. SES templating will quietly fail
    if template variables are missing in expected shapes.
    """

    order = {"Order": {"order_id": 161}}
    bad_order_id = 161
    good_order_id = "string"

    def test_orders_order_crm_update_missing_id(self):
        with self.assertRaises(ArcimotoArgumentError):
            orders_functions.order_crm_update({"order": self.order})

    def test_orders_order_crm_update_bad_id_format(self):
        with self.assertRaises(ArcimotoArgumentError):
            orders_functions.order_crm_update({"order": self.order, "order_id": self.bad_order_id})

    def test_orders_order_crm_update_missing_order(self):
        with self.assertRaises(ArcimotoArgumentError):
            orders_functions.order_crm_update({"order_id": self.good_order_id})


@arcimoto.runtime.handler
def test_orders_order_crm_update():

    return arcimoto.tests.handle_test_result(unittest.TextTestRunner().run(
        unittest.TestLoader().loadTestsFromTestCase(OrdersOrderCrmUpdateTestCase)
    ))


lambda_handler = test_orders_order_crm_update
