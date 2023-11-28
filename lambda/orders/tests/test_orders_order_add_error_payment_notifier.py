import unittest

from arcimoto.exceptions import *
import arcimoto.runtime
import arcimoto.tests
import orders_functions


class OrdersOrderAddErrorPaymentNotifier(unittest.TestCase):

    good_id = "goodorder"
    dict_id = {"dict": "bad format"}
    order = {"order": "order"}

    def test_orders_order_add_error_payment_notifier_missing_id(self):
        with self.assertRaises(ArcimotoArgumentError):
            orders_functions.order_add_error_payment_notifier({"order": self.order})

    def test_orders_order_add_error_payment_notifier_bad_id(self):
        with self.assertRaises(ArcimotoArgumentError):
            orders_functions.order_add_error_payment_notifier({"order_id": self.dict_id, "order": self.order})

    def test_orders_order_add_error_payment_notifier_missing_order(self):
        with self.assertRaises(ArcimotoArgumentError):
            orders_functions.order_add_error_payment_notifier({"order_id": self.good_id})


@arcimoto.runtime.handler
def test_orders_order_add_error_payment_notifier():

    return arcimoto.tests.handle_test_result(unittest.TextTestRunner().run(
        unittest.TestLoader().loadTestsFromTestCase(OrdersOrderAddErrorPaymentNotifier)
    ))


lambda_handler = test_orders_order_add_error_payment_notifier
