import logging
import unittest


from arcimoto.exceptions import *
import arcimoto.runtime
import arcimoto.tests
import vehicles_functions

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class UpdateShadowDocumentTestCase(unittest.TestCase):

    @property
    def vin_invalid(self):
        return arcimoto.tests.uuid_vin_get()

    @classmethod
    def setUpClass(cls):
        cls.vin = arcimoto.tests.uuid_vin_get()
        arcimoto.tests.vehicle_create(cls.vin)
        vehicles_functions.provision_iot(cls.vin)
        vehicles_functions.provision_iot_certificate(cls.vin)

    @classmethod
    def tearDownClass(cls):
        vehicles_functions.unprovision_iot_certificate(cls.vin)
        vehicles_functions.unprovision_iot(cls.vin)
        arcimoto.tests.vehicle_delete(cls.vin)

    def test_update_shadow_document_success(self):
        self.assertIsInstance(vehicles_functions.update_shadow_document(self.vin), dict)

    # test errors
    def test_update_shadow_document_error_input_null_vin(self):
        with self.assertRaises(ArcimotoArgumentError):
            vehicles_functions.update_shadow_document(None)

    def test_update_shadow_document_error_input_invalid_vin(self):
        with self.assertRaises(ArcimotoNotFoundError):
            vehicles_functions.update_shadow_document(self.vin_invalid)


@arcimoto.runtime.handler
def test_update_shadow_document():
    return arcimoto.tests.handle_test_result(unittest.TextTestRunner().run(
        unittest.TestLoader().loadTestsFromTestCase(UpdateShadowDocumentTestCase)
    ))


lambda_handler = test_update_shadow_document
