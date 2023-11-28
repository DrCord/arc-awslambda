import logging
import unittest

from arcimoto.exceptions import *
import arcimoto.runtime
import arcimoto.tests
import authorities_functions

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class GetAuthorityTestCase(unittest.TestCase):

    @property
    def authority_id_invalid(self):
        return authorities_functions.authorities_highest_id() + 1

    @classmethod
    def setUpClass(cls):
        cls.authority_id = authorities_functions.create_authority().get('id', None)

    @classmethod
    def tearDownClass(cls):
        if cls.authority_id is not None:
            authorities_functions.delete_authority(cls.authority_id)

    def test_get_authority_success(self):
        self.assertIsInstance(authorities_functions.get_authority(self.authority_id), dict)

    # test errors
    def test_get_authority_error_no_authority_id(self):
        with self.assertRaises(ArcimotoArgumentError):
            authorities_functions.get_authority(None)

    def test_get_authority_error_authority_id_does_not_exist(self):
        with self.assertRaises(ArcimotoArgumentError):
            authorities_functions.get_authority(self.authority_id_invalid)

    def test_get_authority_error_user_unauthorized(self):
        with self.assertRaises(ArcimotoPermissionError):
            authorities_functions.get_authority(self.authority_id, False)


@arcimoto.runtime.handler
def test_get_authority():
    return arcimoto.tests.handle_test_result(
        unittest.TextTestRunner().run(
            unittest.TestLoader().loadTestsFromTestCase(GetAuthorityTestCase)
        ))


lambda_handler = test_get_authority
