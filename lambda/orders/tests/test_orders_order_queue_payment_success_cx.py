import unittest

from arcimoto.exceptions import *
import arcimoto.runtime
import arcimoto.tests
import orders_functions


class OrdersOrderQueuePaymentSuccessCx(unittest.TestCase):

    def test_orders_order_queue_payment_success_cx_missing_record(self):
        with self.assertRaises(ArcimotoArgumentError):
            orders_functions.order_queue_payment_success_cx({})


@arcimoto.runtime.handler
def test_orders_order_queue_payment_success_cx():
    return arcimoto.tests.handle_test_result(unittest.TextTestRunner().run(
        unittest.TestLoader().loadTestsFromTestCase(OrdersOrderQueuePaymentSuccessCx)
    ))


lambda_handler = test_orders_order_queue_payment_success_cx
