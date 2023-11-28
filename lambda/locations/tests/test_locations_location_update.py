import logging
import unittest
import copy

from arcimoto.exceptions import *
import arcimoto.runtime
import arcimoto.tests
import locations_functions

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class LocationsLocationUpdateTestCase(unittest.TestCase):

    location_id = None
    args = {
        'id': 1,
        'location_name': 'Unit Test Headquarters',
        'street_number': 1234,
        'structure_name': 'Test-Eddifice',
        'street_number_suffix': 'A',
        'street_name': 'Update',
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
        cls.args['id'] = cls.location_id

    @classmethod
    def tearDownClass(cls):
        if cls.location_id is not None:
            locations_functions.location_delete(cls.location_id)

    def test_locations_location_update_success(self):
        self.assertIsInstance(locations_functions.location_update(self.args), dict)

    # test errors
    def test_locations_location_update_error_input_invalid_type_id(self):
        args = copy.deepcopy(self.args)
        args['id'] = 'not an integer'
        with self.assertRaises(ArcimotoArgumentError):
            locations_functions.location_update(args)

    def test_locations_location_update_error_input_invalid_id_min(self):
        args = copy.deepcopy(self.args)
        args['id'] = -1
        with self.assertRaises(ArcimotoArgumentError):
            locations_functions.location_update(args)

    def test_locations_location_update_error_input_invalid_id(self):
        args = copy.deepcopy(self.args)
        args['id'] = locations_functions.locations_get_highest_id() + 1
        with self.assertRaises(ArcimotoException):
            locations_functions.location_update(args)

    def test_locations_location_update_error_input_invalid_location_name_null(self):
        args = copy.deepcopy(self.args)
        args['location_name'] = None
        with self.assertRaises(ArcimotoArgumentError):
            locations_functions.location_update(args)

    def test_locations_location_update_error_input_invalid_location_name_empty(self):
        args = copy.deepcopy(self.args)
        args['location_name'] = ''
        with self.assertRaises(ArcimotoArgumentError):
            locations_functions.location_update(args)

    def test_locations_location_update_error_input_invalid_type_location_name(self):
        args = copy.deepcopy(self.args)
        args['location_name'] = 1
        with self.assertRaises(ArcimotoArgumentError):
            locations_functions.location_update(args)

    def test_locations_location_update_error_input_invalid_type_street_number(self):
        args = copy.deepcopy(self.args)
        args['street_number'] = 'not an integer'
        with self.assertRaises(ArcimotoArgumentError):
            locations_functions.location_update(args)

    def test_locations_location_update_error_input_invalid_type_structure_name(self):
        args = copy.deepcopy(self.args)
        args['structure_name'] = 1
        with self.assertRaises(ArcimotoArgumentError):
            locations_functions.location_update(args)

    def test_locations_location_update_error_input_invalid_type_street_number_suffix(self):
        args = copy.deepcopy(self.args)
        args['street_number_suffix'] = 1
        with self.assertRaises(ArcimotoArgumentError):
            locations_functions.location_update(args)

    def test_locations_location_update_error_input_invalid_type_street_name(self):
        args = copy.deepcopy(self.args)
        args['street_name'] = 1
        with self.assertRaises(ArcimotoArgumentError):
            locations_functions.location_update(args)

    def test_locations_location_update_error_input_invalid_type_street_type(self):
        args = copy.deepcopy(self.args)
        args['street_type'] = 1
        with self.assertRaises(ArcimotoArgumentError):
            locations_functions.location_update(args)

    def test_locations_location_update_error_input_invalid_type_street_direction(self):
        args = copy.deepcopy(self.args)
        args['street_direction'] = 1
        with self.assertRaises(ArcimotoArgumentError):
            locations_functions.location_update(args)

    def test_locations_location_update_error_input_invalid_type_address_type(self):
        args = copy.deepcopy(self.args)
        args['address_type'] = 'not an integer'
        with self.assertRaises(ArcimotoArgumentError):
            locations_functions.location_update(args)

    def test_locations_location_update_error_input_invalid_type_address_type_identifier(self):
        args = copy.deepcopy(self.args)
        args['address_type_identifier'] = 1
        with self.assertRaises(ArcimotoArgumentError):
            locations_functions.location_update(args)

    def test_locations_location_update_error_input_invalid_type_city(self):
        args = copy.deepcopy(self.args)
        args['city'] = 1
        with self.assertRaises(ArcimotoArgumentError):
            locations_functions.location_update(args)

    def test_locations_location_update_error_input_invalid_type_governing_district(self):
        args = copy.deepcopy(self.args)
        args['governing_district'] = 1
        with self.assertRaises(ArcimotoArgumentError):
            locations_functions.location_update(args)

    def test_locations_location_update_error_input_invalid_type_postal_area(self):
        args = copy.deepcopy(self.args)
        args['postal_area'] = 1
        with self.assertRaises(ArcimotoArgumentError):
            locations_functions.location_update(args)

    def test_locations_location_update_error_input_invalid_type_local_municipality(self):
        args = copy.deepcopy(self.args)
        args['local_municipality'] = 1
        with self.assertRaises(ArcimotoArgumentError):
            locations_functions.location_update(args)

    def test_locations_location_update_error_input_invalid_type_country(self):
        args = copy.deepcopy(self.args)
        args['country'] = 1
        with self.assertRaises(ArcimotoArgumentError):
            locations_functions.location_update(args)

    def test_locations_location_update_error_input_invalid_type_gps_latitude(self):
        args = copy.deepcopy(self.args)
        args['gps_latitude'] = 'not a float'
        with self.assertRaises(ArcimotoArgumentError):
            locations_functions.location_update(args)

    def test_locations_location_update_error_input_invalid_type_gps_longitude(self):
        args = copy.deepcopy(self.args)
        args['gps_longitude'] = 'not a float'
        with self.assertRaises(ArcimotoArgumentError):
            locations_functions.location_update(args)

    def test_locations_location_update_error_input_invalid_address_type(self):
        args = copy.deepcopy(self.args)
        args['address_type'] = locations_functions.address_types_get_highest_id() + 1
        with self.assertRaises(ArcimotoException):
            locations_functions.location_update(args)

    def test_locations_location_update_error_input_invalid_country(self):
        args = copy.deepcopy(self.args)
        args['country'] = 'XX'
        with self.assertRaises(ArcimotoArgumentError):
            locations_functions.location_update(args)

    def test_locations_location_update_error_input_invalid_country_length(self):
        args = copy.deepcopy(self.args)
        args['country'] = 'USA'
        with self.assertRaises(ArcimotoArgumentError):
            locations_functions.location_update(args)

    def test_locations_location_update_error_user_unauthorized(self):
        with self.assertRaises(ArcimotoPermissionError):
            locations_functions.location_update(self.args, False)


@arcimoto.runtime.handler
def test_locations_location_update():
    return arcimoto.tests.handle_test_result(unittest.TextTestRunner().run(
        unittest.TestLoader().loadTestsFromTestCase(LocationsLocationUpdateTestCase)
    ))


lambda_handler = test_locations_location_update
