import unittest

from arcimoto.exceptions import *
import arcimoto.runtime
import arcimoto.tests
import orders_functions


class OrdersOrderGetTestCase(unittest.TestCase):

    order_id = None

    @classmethod
    def setUpClass(cls):
        response = orders_functions.order_create(orders_functions.order_get_test_dict())
        cls.order_id = response.get('id', None)
        if cls.order_id is None:
            raise ArcimotoException(f'Unable to create order for Get unit tests setup')

    @classmethod
    def tearDownClass(cls):
        if cls.order_id is not None:
            orders_functions.order_delete({"order_id": cls.order_id})

    def test_orders_order_get_success(self):
        result = orders_functions.order_get({"order_id": self.order_id})
        self.assertIsNotNone(result)

    def test_orders_order_get_error_input_null_id(self):
        with self.assertRaises(AttributeError):
            orders_functions.order_get(None)

    def test_orders_order_get_error_input_invalid_type_id(self):
        with self.assertRaises(ArcimotoArgumentError):
            orders_functions.order_get({"order_id": {"dict": "A dict is an invalid id"}})

    def test_orders_order_get_error_input_id_None(self):
        with self.assertRaises(ArcimotoArgumentError):
            orders_functions.order_get({"order_id": None})


@arcimoto.runtime.handler
def test_orders_order_get():
    return arcimoto.tests.handle_test_result(unittest.TextTestRunner().run(
        unittest.TestLoader().loadTestsFromTestCase(OrdersOrderGetTestCase)
    ))


lambda_handler = test_orders_order_get
