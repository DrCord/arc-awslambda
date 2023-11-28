import unittest

from arcimoto.exceptions import *
import arcimoto.runtime
import arcimoto.tests
import orders_functions


class OrdersOrderAddSuccessPaymentNotifier(unittest.TestCase):

    good_id = 161
    bad_id = -1
    good_order = {"order": "test"}

    def test_orders_order_add_success_payment_notifier_missing_id(self):
        with self.assertRaises(ArcimotoArgumentError):
            orders_functions.order_add_success_payment_notifier({"order": self.good_order})

    def test_orders_order_add_success_payment_notifier_bad_id(self):
        with self.assertRaises(ArcimotoArgumentError):
            orders_functions.order_add_success_payment_notifier({"order_id": self.bad_id, "order": self.good_order})

    def test_orders_order_add_success_payment_notifier_missing_order(self):
        with self.assertRaises(ArcimotoArgumentError):
            orders_functions.order_add_success_payment_notifier({"order_id": self.good_id})


@arcimoto.runtime.handler
def test_orders_order_add_success_payment_notifier():

    return arcimoto.tests.handle_test_result(unittest.TextTestRunner().run(
        unittest.TestLoader().loadTestsFromTestCase(OrdersOrderAddSuccessPaymentNotifier)
    ))


lambda_handler = test_orders_order_add_success_payment_notifier
