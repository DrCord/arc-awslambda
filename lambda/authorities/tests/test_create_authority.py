import logging
import unittest

from arcimoto.exceptions import *
import arcimoto.runtime
import arcimoto.tests
import authorities_functions

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class CreateAuthorityTestCase(unittest.TestCase):

    @property
    def authority_id_invalid(self):
        return authorities_functions.authorities_highest_id() + 1

    def test_create_authority_success(self):
        authority = authorities_functions.create_authority()
        self.assertIsInstance(authority, dict)
        authority_id = authority.get('id', None)
        if authority_id is not None:
            authorities_functions.delete_authority(authority_id)

    # test errors
    def test_create_authority_error_null_description(self):
        with self.assertRaises(ArcimotoArgumentError):
            authorities_functions.create_authority(None)

    def test_create_authority_error_parent_authority_id_does_not_exist(self):
        with self.assertRaises(ArcimotoNotFoundError):
            authorities_functions.create_authority('Unit Tester', self.authority_id_invalid)

    def test_create_authority_error_user_unauthorized(self):
        with self.assertRaises(ArcimotoPermissionError):
            authorities_functions.create_authority('Unit Tester', None, None, False)


@arcimoto.runtime.handler
def test_create_authority():
    return arcimoto.tests.handle_test_result(
        unittest.TextTestRunner().run(
            unittest.TestLoader().loadTestsFromTestCase(CreateAuthorityTestCase)
        ))


lambda_handler = test_create_authority
