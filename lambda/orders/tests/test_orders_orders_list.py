import unittest

from arcimoto.exceptions import *
import arcimoto.runtime
import arcimoto.tests
import orders_functions


class OrdersOrdersListTestCase(unittest.TestCase):

    def test_orders_list_success(self):
        result = orders_functions.orders_list()
        self.assertTrue(isinstance(result.get('orders'), list))


@arcimoto.runtime.handler
def test_orders_orders_list():

    return arcimoto.tests.handle_test_result(unittest.TextTestRunner().run(
        unittest.TestLoader().loadTestsFromTestCase(OrdersOrdersListTestCase)
    ))


lambda_handler = test_orders_orders_list
