import logging
import unittest

from arcimoto.exceptions import *
import arcimoto.runtime
import arcimoto.tests
import authorities_functions

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class ListAuthoritiesTestCase(unittest.TestCase):

    @property
    def authorities_list_len(self):
        return len(authorities_functions.list_authorities())

    @classmethod
    def setUpClass(cls):
        cls.vin = arcimoto.tests.uuid_vin_get()
        cls.test_authority_id = authorities_functions.create_authority().get('id', None)
        cls.test_authority_id2 = authorities_functions.create_authority('Unit Tester 2', cls.test_authority_id).get('id', None)
        authorities_functions.provision_vehicle_authority(authorities_functions.ARCIMOTO_AUTHORITY_ID, cls.vin)
        authorities_functions.provision_vehicle_authority(cls.test_authority_id, cls.vin)

    @classmethod
    def tearDownClass(cls):
        if cls.test_authority_id2 is not None:
            authorities_functions.delete_authority(cls.test_authority_id2)
        if cls.test_authority_id is not None:
            authorities_functions.unprovision_vehicle_authority(cls.test_authority_id, cls.vin)
            authorities_functions.delete_authority(cls.test_authority_id)

    def test_list_authorities_success_no_input(self):
        self.assertIsInstance(authorities_functions.list_authorities(), list)

    def test_list_authorities_success_filter_args_id(self):
        self.assertTrue(len(authorities_functions.list_authorities({'id': self.test_authority_id})) == 1)

    def test_list_authorities_success_filter_args_parent_id(self):
        self.assertTrue(len(authorities_functions.list_authorities({'parent_id': self.test_authority_id})) == 1)

    def test_list_authorities_success_filter_args_description(self):
        self.assertTrue(0 < len(authorities_functions.list_authorities({'description': 'Unit Tester'})) < self.authorities_list_len)

    def test_list_authorities_success_include_vin(self):
        authorities_list = authorities_functions.list_authorities(None, True)
        authority = next((item for item in authorities_list if item['id'] == self.test_authority_id), None)
        self.assertTrue(authority.get('vins', None))

    # test errors
    def test_list_authorities_error_user_unauthorized(self):
        with self.assertRaises(ArcimotoPermissionError):
            authorities_functions.list_authorities(None, None, False)


@arcimoto.runtime.handler
def test_list_authorities():
    return arcimoto.tests.handle_test_result(
        unittest.TextTestRunner().run(
            unittest.TestLoader().loadTestsFromTestCase(ListAuthoritiesTestCase)
        ))


lambda_handler = test_list_authorities
