import logging
import unittest

from arcimoto.exceptions import *
import arcimoto.runtime
import arcimoto.tests
import authorities_functions

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class DeleteAuthorityTestCase(unittest.TestCase):

    @property
    def authority_id_invalid(self):
        return authorities_functions.authorities_highest_id() + 1

    @classmethod
    def setUpClass(cls):
        cls.authority = authorities_functions.create_authority()
        cls.authority_id = cls.authority.get('id', None)

    def test_delete_authority_success(self):
        self.assertIsInstance(authorities_functions.delete_authority(self.authority_id), dict)

    # test errors
    def test_delete_authority_error_no_authority_id(self):
        with self.assertRaises(ArcimotoArgumentError):
            authorities_functions.delete_authority(None)

    def test_delete_authority_error_not_postive_integer(self):
        with self.assertRaises(ArcimotoArgumentError):
            authorities_functions.delete_authority(-1)

    def test_delete_authority_error_cannot_delete_arcimoto_authority(self):
        with self.assertRaises(ArcimotoArgumentError):
            authorities_functions.delete_authority(1)

    def test_delete_authority_error_authority_id_does_not_exist(self):
        with self.assertRaises(ArcimotoNotFoundError):
            authorities_functions.delete_authority(self.authority_id_invalid)

    def test_delete_authority_error_user_unauthorized(self):
        with self.assertRaises(ArcimotoPermissionError):
            authorities_functions.delete_authority(self.authority_id, False)


@arcimoto.runtime.handler
def test_delete_authority():
    return arcimoto.tests.handle_test_result(
        unittest.TextTestRunner().run(
            unittest.TestLoader().loadTestsFromTestCase(DeleteAuthorityTestCase)
        ))


lambda_handler = test_delete_authority
