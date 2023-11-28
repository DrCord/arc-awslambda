import unittest

from arcimoto.exceptions import *
import arcimoto.runtime
import arcimoto.tests
import orders_functions


class OrdersOrderCreateTestCase(unittest.TestCase):

    order_id = None

    @classmethod
    def setUpClass(cls):
        result = orders_functions.order_create(orders_functions.order_get_test_dict())
        cls.order_id = result['id']

    @classmethod
    def tearDownClass(cls):
        orders_functions.order_delete({'order_id': cls.order_id})

    @arcimoto.db.transaction
    def test_order_create_success(self):
        result = orders_functions.order_get({'order_id': self.order_id})
        self.assertEqual(result[0], self.order_id)

    def test_order_create_error_input_null_request(self):
        with self.assertRaises(ArcimotoArgumentError):
            orders_functions.order_create({'order_request': None})

    def test_order_create_error_input_invalid_type_request(self):
        with self.assertRaises(Exception):
            orders_functions.order_create('Invalid Input')


@arcimoto.runtime.handler
def test_orders_order_create():

    return arcimoto.tests.handle_test_result(unittest.TextTestRunner().run(
        unittest.TestLoader().loadTestsFromTestCase(OrdersOrderCreateTestCase)
    ))


lambda_handler = test_orders_order_create
