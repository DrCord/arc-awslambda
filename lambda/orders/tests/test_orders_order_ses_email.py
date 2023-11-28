import unittest

from arcimoto.exceptions import *
import arcimoto.runtime
import arcimoto.tests
import orders_functions


class OrdersOrderSesEmailTestCase(unittest.TestCase):
    """
    Important Note: Order form should be validated at Order Create. SES templating will quietly fail
    if template variables are missing in expected shapes.
    """

    order = {"Order": {"order_id": 161}}
    order_id = 161
    good_target = 'CX_SUCCESS'

    def test_orders_order_ses_email_missing_id(self):
        with self.assertRaises(ArcimotoArgumentError):
            orders_functions.order_ses_email({"order": self.order, "target": self.good_target})

    def test_orders_order_ses_email_bad_id_format(self):
        with self.assertRaises(ArcimotoArgumentError):
            orders_functions.order_ses_email({"order": {"dict": "bad id format"}, "target": self.good_target})

    def test_orders_order_ses_email_missing_target(self):
        with self.assertRaises(ArcimotoArgumentError):
            orders_functions.order_ses_email({"order": self.order, "order_id": self.order_id})

    def test_orders_order_ses_email_missing_order(self):
        with self.assertRaises(ArcimotoArgumentError):
            orders_functions.order_ses_email({"order_id": self.order_id, "target": self.good_target})


@arcimoto.runtime.handler
def test_orders_order_ses_email():

    return arcimoto.tests.handle_test_result(unittest.TextTestRunner().run(
        unittest.TestLoader().loadTestsFromTestCase(OrdersOrderSesEmailTestCase)
    ))


lambda_handler = test_orders_order_ses_email
