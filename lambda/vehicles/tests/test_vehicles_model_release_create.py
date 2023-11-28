import logging
import unittest
import copy
import uuid

from arcimoto.exceptions import *
import arcimoto.runtime
import arcimoto.tests
import vehicles_functions

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class VehiclesModelReleaseCreateTestCase(unittest.TestCase):

    MODEL_ID = 1
    description = 'FUV: created during unit tests for vehicles_model_release_create'
    # actual parts config for `KERS Sensor` model releases
    # with "-{UUID}" appended to VCU to set new part number for to get unique configuration
    parts = {
        'BMS': '001052',
        'Charger': '001940',
        'Comm': '004280',
        'Display': '004280',
        'EPSU': '001960',
        'H Bridge': '003223',
        'Inverter - Left': '004085',
        'Inverter - Right': '004085',
        'IO Front': '003225',
        'IO Rear': '003224',
        'KERS Sensor': '001412',
        'LV': '004313',
        'VCU': '003222' + '-' + uuid.uuid4().hex
    }

    def test_vehicles_model_release_create_success(self):

        @arcimoto.db.transaction
        def cleanup(model_release_id):
            # cleanup after success
            cursor = arcimoto.db.get_cursor()

            query = (
                'DELETE FROM vehicle_model_parts '
                'WHERE model_release_id = %s'
            )
            cursor.execute(query, [model_release_id])

            query = (
                'DELETE FROM vehicle_model_release '
                'WHERE model_release_id = %s'
            )
            cursor.execute(query, [model_release_id])

        result = vehicles_functions.model_release_create(self.MODEL_ID, self.description, self.parts)
        model_release_id = result.get('model_release_id')
        self.assertIsInstance(result, dict)
        cleanup(model_release_id)

    # test errors
    def test_vehicles_model_release_create_error_null_model_id(self):
        with self.assertRaises(ArcimotoArgumentError):
            vehicles_functions.model_release_create(None, self.description, self.parts)

    def test_vehicles_model_release_create_error_null_description(self):
        with self.assertRaises(ArcimotoArgumentError):
            vehicles_functions.model_release_create(self.MODEL_ID, None, self.parts)

    def test_vehicles_model_release_create_error_null_parts(self):
        with self.assertRaises(ArcimotoArgumentError):
            vehicles_functions.model_release_create(self.MODEL_ID, self.description, None)

    def test_vehicles_model_release_create_error_invalid_model_id_min(self):
        with self.assertRaises(ArcimotoArgumentError):
            vehicles_functions.model_release_create(-1, self.description, self.parts)

    def test_vehicles_model_release_create_error_invalid_model_id_does_not_exist(self):
        with self.assertRaises(ArcimotoArgumentError):
            vehicles_functions.model_release_create(100000000, self.description, self.parts)

    def test_vehicles_model_release_create_error_invalid_type_model_release_id(self):
        with self.assertRaises(ArcimotoArgumentError):
            vehicles_functions.model_release_create('not an integer', self.description, self.parts)

    def test_vehicles_model_release_create_error_invalid_type_description(self):
        with self.assertRaises(ArcimotoArgumentError):
            vehicles_functions.model_release_create(self.MODEL_ID, 1, self.parts)

    def test_vehicles_model_release_create_error_invalid_type_parts(self):
        with self.assertRaises(ArcimotoArgumentError):
            vehicles_functions.model_release_create(self.MODEL_ID, self.description, 'not a dictionary')

    def test_vehicles_model_release_create_error_invalid_parts_config_already_exists_for_model_id(self):
        # set to an existing parts configuration to force fail for test
        parts = copy.deepcopy(self.parts)
        parts['VCU'] = '003222'
        with self.assertRaises(ArcimotoArgumentError):
            vehicles_functions.model_release_create(self.MODEL_ID, self.description, parts)

    def test_vehicles_model_release_create_error_unauthorized(self):
        with self.assertRaises(ArcimotoPermissionError):
            vehicles_functions.model_release_create(self.MODEL_ID, self.description, self.parts, False)


@arcimoto.runtime.handler
def test_vehicles_model_release_create():
    return arcimoto.tests.handle_test_result(unittest.TextTestRunner().run(
        unittest.TestLoader().loadTestsFromTestCase(VehiclesModelReleaseCreateTestCase)
    ))


lambda_handler = test_vehicles_model_release_create
