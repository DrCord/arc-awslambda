import logging
import unittest

from arcimoto.exceptions import *
import arcimoto.runtime
import arcimoto.tests
import authorities_functions

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class RekeyAuthorityTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.authority_id = authorities_functions.create_authority().get('id', None)

    @classmethod
    def tearDownClass(cls):
        if cls.authority_id is not None:
            authorities_functions.delete_authority(cls.authority_id)

    def test_rekey_authority_success(self):
        self.assertIsInstance(authorities_functions.rekey_authority(self.authority_id), dict)

    # test errors
    def test_rekey_authority_error_no_authority_id(self):
        with self.assertRaises(ArcimotoArgumentError):
            authorities_functions.rekey_authority(None)

    def test_rekey_authority_error_user_unauthorized(self):
        with self.assertRaises(ArcimotoPermissionError):
            authorities_functions.rekey_authority(self.authority_id, False)

    # not testable errors
    # rekey check didn't match exactly one authority
    # rekey update didn't match exactly one authority


@arcimoto.runtime.handler
def test_rekey_authority():
    return arcimoto.tests.handle_test_result(
        unittest.TextTestRunner().run(
            unittest.TestLoader().loadTestsFromTestCase(RekeyAuthorityTestCase)
        ))


lambda_handler = test_rekey_authority
