import unittest

from arcimoto.exceptions import *
import arcimoto.runtime
import arcimoto.tests
import orders_functions


class OrdersOrderDeleteTestCase(unittest.TestCase):

    order_id = None

    @classmethod
    def setUpClass(cls):
        response = orders_functions.order_create(orders_functions.order_get_test_dict())
        cls.order_id = response.get('id', None)
        if cls.order_id is None:
            raise ArcimotoException(f'Unable to create order for delete unit tests setup')

    @classmethod
    def tearDownClass(cls):
        if cls.order_id is not None:
            orders_functions.order_delete({"order_id": cls.order_id})

    def test_orders_order_delete_success(self):
        result = orders_functions.order_get({"order_id": self.order_id})
        self.assertIsNotNone(result)
        result = orders_functions.order_delete({"order_id": self.order_id})
        self.assertEqual(result.get("deleted_rows"), 1)

    def test_orders_order_delete_error_input_null_id(self):
        with self.assertRaises(ArcimotoArgumentError):
            orders_functions.order_delete({"order_id": None})

    def test_orders_order_delete_bad_format_id(self):
        with self.assertRaises(ArcimotoArgumentError):
            orders_functions.order_delete({"order_id": {"dict": "bad format"}})


@arcimoto.runtime.handler
def test_orders_order_delete():
    return arcimoto.tests.handle_test_result(unittest.TextTestRunner().run(
        unittest.TestLoader().loadTestsFromTestCase(OrdersOrderDeleteTestCase)
    ))


lambda_handler = test_orders_order_delete
