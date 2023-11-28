from datetime import datetime
import unittest

from arcimoto.exceptions import *
import arcimoto.runtime
import arcimoto.tests
import orders_functions


class OrdersOrderArchiveTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        result = orders_functions.order_create(orders_functions.order_get_test_dict())
        cls.order_id = result['id']

    @classmethod
    def tearDownClass(cls):
        orders_functions.order_delete({'order_id': cls.order_id})

    def test_order_archive_success(self):
        archived_order = orders_functions.order_archive({'order_id': self.order_id})
        d = datetime.strptime(archived_order.get('archived_at'), '%Y-%m-%d %H:%M:%S.%f')
        assert isinstance(d, datetime)

    def test_order_archive_z_already_archived(self):
        self.assertFalse(orders_functions.order_archive({'order_id': self.order_id}))

    def test_order_archive_error_invalid_id(self):
        self.assertFalse(orders_functions.order_archive({"order_id": "bad_id"}))

    def test_order_archive_error_invalid_id_type(self):
        with self.assertRaises(ArcimotoArgumentError):
            orders_functions.order_archive({"order_id": {"dict": "bad format"}})


@arcimoto.runtime.handler
def test_orders_order_archive():

    return arcimoto.tests.handle_test_result(unittest.TextTestRunner().run(
        unittest.TestLoader().loadTestsFromTestCase(OrdersOrderArchiveTestCase)
    ))


lambda_handler = test_orders_order_archive
