import unittest
import copy

from arcimoto.exceptions import *
import arcimoto.runtime
import arcimoto.tests
import orders_functions


class OrdersOrderAddPaymentTestCase(unittest.TestCase):

    payment = {
        "amount": 508,
        "status": "approved",
        "provider": "authnet",
        "paymentMethod": "ach",
        "transactionId": "60193943273"
    }

    bad_payment = 'paymentStr'

    order_id = None

    @classmethod
    def setUpClass(cls):
        result = orders_functions.order_create(orders_functions.order_get_test_dict())
        cls.order_id = result['id']

    @classmethod
    def tearDownClass(cls):
        orders_functions.order_delete({'order_id': cls.order_id})

    def test_order_add_payment_success(self):
        result = orders_functions.order_add_payment({'order_id': self.order_id, 'payment': self.payment})
        self.assertTrue(result['order_request'].get('payment') == self.payment)

    def test_order_add_payment_invalid_input_payment(self):
        with self.assertRaises(AttributeError):
            orders_functions.order_add_payment(self.bad_payment)

    def test_order_add_payment_invalid_input_order_id(self):
        with self.assertRaises(ArcimotoArgumentError):
            orders_functions.order_add_payment({'order_id': {"dict": "bad type"}, 'payment': self.payment})

    def test_order_add_payment_missing_input_payment(self):
        with self.assertRaises(AttributeError):
            orders_functions.order_add_payment(None)

    def test_order_add_payment_bad_amount(self):
        order_bad_amount = copy.deepcopy(self.payment)
        order_bad_amount['amount'] = 'not a number'
        with self.assertRaises(ArcimotoArgumentError):
            orders_functions.order_add_payment({'order_id': self.order_id, 'payment': order_bad_amount})

    def test_order_add_payment_bad_status(self):
        order_bad_status = copy.deepcopy(self.payment)
        order_bad_status['status'] = 'not a good status'
        with self.assertRaises(ArcimotoArgumentError):
            orders_functions.order_add_payment({'order_id': self.order_id, 'payment': order_bad_status})


@arcimoto.runtime.handler
def test_orders_order_add_payment():

    return arcimoto.tests.handle_test_result(unittest.TextTestRunner().run(
        unittest.TestLoader().loadTestsFromTestCase(OrdersOrderAddPaymentTestCase)
    ))


lambda_handler = test_orders_order_add_payment
