import logging
import unittest
import uuid

from arcimoto.exceptions import *
import arcimoto.runtime
import arcimoto.tests
import vehicles_functions

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class VehiclesPartTypeCreateTestCase(unittest.TestCase):

    part_type = 'Unit Test Part Type'

    @classmethod
    def tearDownClass(cls):

        @arcimoto.db.transaction
        def cleanup():
            cursor = arcimoto.db.get_cursor()

            query = (
                'DELETE FROM vehicle_part_types '
                'WHERE part_type = %s'
            )
            cursor.execute(query, [cls.part_type])
        cleanup()

    def test_vehicles_part_type_create_success(self):
        self.assertIsInstance(vehicles_functions.part_type_create(self.part_type), dict)

    # test errors
    def test_vehicles_part_type_create_error_null_part_type(self):
        with self.assertRaises(ArcimotoArgumentError):
            vehicles_functions.part_type_create(None)

    def test_vehicles_part_type_create_error_invalid_type_part_type(self):
        with self.assertRaises(ArcimotoArgumentError):
            vehicles_functions.part_type_create(1)

    def test_vehicles_part_type_create_error_unauthorized(self):
        with self.assertRaises(ArcimotoPermissionError):
            vehicles_functions.part_type_create(self.part_type, False)


@arcimoto.runtime.handler
def test_vehicles_part_type_create():
    return arcimoto.tests.handle_test_result(unittest.TextTestRunner().run(
        unittest.TestLoader().loadTestsFromTestCase(VehiclesPartTypeCreateTestCase)
    ))


lambda_handler = test_vehicles_part_type_create
