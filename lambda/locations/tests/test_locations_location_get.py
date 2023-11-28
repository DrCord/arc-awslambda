import logging
import unittest


from arcimoto.exceptions import *
import arcimoto.runtime
import arcimoto.tests
import locations_functions

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class LocationsLocationGetTestCase(unittest.TestCase):

    location_id = None
    args = {
        'id': 1,
        'location_name': 'Unit Test Headquarters',
        'street_number': 1234,
        'structure_name': 'Test-Eddifice',
        'street_number_suffix': 'A',
        'street_name': 'Get',
        'street_type': 'Row',
        'street_direction': 'NE',
        'address_type': 1,
        'address_type_identifier': '5678',
        'city': 'Smalltown',
        'governing_district': 'Pennsylvania',
        'postal_area': '12345',
        'local_municipality': 'Village Green',
        'country': 'US',
        'gps_latitude': -123.0054,
        'gps_longitude': 123.0054
    }

    @classmethod
    def setUpClass(cls):
        response = locations_functions.location_create(cls.args)
        cls.location_id = response.get('id', None)
        if cls.location_id is None:
            raise ArcimotoException('Unable to create location for unit tests setup')

    @classmethod
    def tearDownClass(cls):
        if cls.location_id is not None:
            locations_functions.location_delete(cls.location_id)

    def test_locations_location_get_success(self):
        self.assertIsInstance(locations_functions.location_get(self.location_id), dict)

    # test errors
    def test_locations_location_get_error_input_null_id(self):
        with self.assertRaises(ArcimotoArgumentError):
            locations_functions.location_get(None)

    def test_locations_location_get_error_input_invalid_type_id(self):
        with self.assertRaises(ArcimotoArgumentError):
            locations_functions.location_get('not an integer')

    def test_locations_location_get_error_input_invalid_id_min(self):
        with self.assertRaises(ArcimotoArgumentError):
            locations_functions.location_get(-1)

    def test_locations_location_get_error_input_invalid_id(self):
        invalid_id = locations_functions.locations_get_highest_id() + 1
        with self.assertRaises(ArcimotoArgumentError):
            locations_functions.location_get(invalid_id)


@arcimoto.runtime.handler
def test_locations_location_get():
    return arcimoto.tests.handle_test_result(unittest.TextTestRunner().run(
        unittest.TestLoader().loadTestsFromTestCase(LocationsLocationGetTestCase)
    ))


lambda_handler = test_locations_location_get
