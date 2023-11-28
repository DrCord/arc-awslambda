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


class LocationsLocationCreateTestCase(unittest.TestCase):

    args = {
        'location_name': 'Unit Test Headquarters',
        'street_number': 1234,
        'structure_name': 'Test-Eddifice',
        'street_number_suffix': 'A',
        'street_name': 'Create',
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

    def test_location_create_success(self):
        response = locations_functions.location_create(self.args)
        location_id = response.get('id', None)
        self.assertIsInstance(response, dict)
        # cleanup - have to do it here as the cls object doesn't know about id if we pass back in self
        if location_id is not None:
            locations_functions.location_delete(location_id)

    # test errors
    def test_location_create_error_input_invalid_type_location_name_null(self):
        args = copy.deepcopy(self.args)
        args['location_name'] = None
        with self.assertRaises(ArcimotoArgumentError):
            locations_functions.location_create(args)

    def test_location_create_error_input_invalid_type_location_name_empty(self):
        args = copy.deepcopy(self.args)
        args['location_name'] = ''
        with self.assertRaises(ArcimotoArgumentError):
            locations_functions.location_create(args)

    def test_location_create_error_input_invalid_type_location_name(self):
        args = copy.deepcopy(self.args)
        args['location_name'] = 1
        with self.assertRaises(ArcimotoArgumentError):
            locations_functions.location_create(args)

    def test_location_create_error_input_invalid_type_street_number(self):
        args = copy.deepcopy(self.args)
        args['street_number'] = 'not an integer'
        with self.assertRaises(ArcimotoArgumentError):
            locations_functions.location_create(args)

    def test_location_create_error_input_invalid_type_structure_name(self):
        args = copy.deepcopy(self.args)
        args['structure_name'] = 1
        with self.assertRaises(ArcimotoArgumentError):
            locations_functions.location_create(args)

    def test_location_create_error_input_invalid_type_street_number_suffix(self):
        args = copy.deepcopy(self.args)
        args['street_number_suffix'] = 1
        with self.assertRaises(ArcimotoArgumentError):
            locations_functions.location_create(args)

    def test_location_create_error_input_invalid_type_street_name(self):
        args = copy.deepcopy(self.args)
        args['street_name'] = 1
        with self.assertRaises(ArcimotoArgumentError):
            locations_functions.location_create(args)

    def test_location_create_error_input_invalid_type_street_type(self):
        args = copy.deepcopy(self.args)
        args['street_type'] = 1
        with self.assertRaises(ArcimotoArgumentError):
            locations_functions.location_create(args)

    def test_location_create_error_input_invalid_type_street_direction(self):
        args = copy.deepcopy(self.args)
        args['street_direction'] = 1
        with self.assertRaises(ArcimotoArgumentError):
            locations_functions.location_create(args)

    def test_location_create_error_input_invalid_type_address_type(self):
        args = copy.deepcopy(self.args)
        args['address_type'] = 'not an integer'
        with self.assertRaises(ArcimotoArgumentError):
            locations_functions.location_create(args)

    def test_location_create_error_input_invalid_type_address_type_identifier(self):
        args = copy.deepcopy(self.args)
        args['address_type_identifier'] = 1
        with self.assertRaises(ArcimotoArgumentError):
            locations_functions.location_create(args)

    def test_location_create_error_input_invalid_type_city(self):
        args = copy.deepcopy(self.args)
        args['city'] = 1
        with self.assertRaises(ArcimotoArgumentError):
            locations_functions.location_create(args)

    def test_location_create_error_input_invalid_type_governing_district(self):
        args = copy.deepcopy(self.args)
        args['governing_district'] = 1
        with self.assertRaises(ArcimotoArgumentError):
            locations_functions.location_create(args)

    def test_location_create_error_input_invalid_type_postal_area(self):
        args = copy.deepcopy(self.args)
        args['postal_area'] = 1
        with self.assertRaises(ArcimotoArgumentError):
            locations_functions.location_create(args)

    def test_location_create_error_input_invalid_type_local_municipality(self):
        args = copy.deepcopy(self.args)
        args['local_municipality'] = 1
        with self.assertRaises(ArcimotoArgumentError):
            locations_functions.location_create(args)

    def test_location_create_error_input_invalid_type_country(self):
        args = copy.deepcopy(self.args)
        args['country'] = 1
        with self.assertRaises(ArcimotoArgumentError):
            locations_functions.location_create(args)

    def test_location_create_error_input_invalid_type_gps_latitude(self):
        args = copy.deepcopy(self.args)
        args['gps_latitude'] = 'not a float'
        with self.assertRaises(ArcimotoArgumentError):
            locations_functions.location_create(args)

    def test_location_create_error_input_invalid_type_gps_longitude(self):
        args = copy.deepcopy(self.args)
        args['gps_longitude'] = 'not a float'
        with self.assertRaises(ArcimotoArgumentError):
            locations_functions.location_create(args)

    def test_location_create_error_input_invalid_address_type(self):
        args = copy.deepcopy(self.args)
        args['address_type'] = locations_functions.address_types_get_highest_id() + 1
        with self.assertRaises(ArcimotoException):
            locations_functions.location_create(args)

    def test_location_create_error_input_invalid_country(self):
        args = copy.deepcopy(self.args)
        args['country'] = 'XX'
        with self.assertRaises(ArcimotoArgumentError):
            locations_functions.location_create(args)

    def test_location_create_error_input_invalid_country_length(self):
        args = copy.deepcopy(self.args)
        args['country'] = 'USA'
        with self.assertRaises(ArcimotoArgumentError):
            locations_functions.location_create(args)


@arcimoto.runtime.handler
def test_location_create():
    return arcimoto.tests.handle_test_result(unittest.TextTestRunner().run(
        unittest.TestLoader().loadTestsFromTestCase(LocationsLocationCreateTestCase)
    ))


lambda_handler = test_location_create
