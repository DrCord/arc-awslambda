import logging
import unittest


from arcimoto.exceptions import *
import arcimoto.runtime
import arcimoto.tests
import authorities_functions

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class FactoryPinGenerateTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.vin = arcimoto.tests.uuid_vin_get()

    def test_factory_pin_generate_success(self):
        self.assertIsInstance(authorities_functions.factory_pin_generate(self.vin), dict)

    def test_factory_pin_generate_success_keep_pin_true(self):
        preserve_pin = True
        original_pin = authorities_functions.factory_pin_generate(self.vin).get('pin')
        new_pin = authorities_functions.factory_pin_keep_pin_generate(self.vin, preserve_pin).get('pin')
        self.assertEqual(original_pin, new_pin)

    def test_factory_pin_generate_success_keep_pin_false(self):
        preserve_pin = False
        original_pin = authorities_functions.factory_pin_generate(self.vin).get('pin')
        new_pin = authorities_functions.factory_pin_keep_pin_generate(self.vin, preserve_pin).get('pin')
        self.assertNotEqual(original_pin, new_pin)

    def test_factory_pin_generate_success_keep_pin_null(self):
        preserve_pin = None
        original_pin = authorities_functions.factory_pin_generate(self.vin).get('pin')
        new_pin = authorities_functions.factory_pin_keep_pin_generate(self.vin, preserve_pin).get('pin')
        self.assertNotEqual(original_pin, new_pin)

    # test errors
    def test_factory_pin_generate_error_input_null_vin(self):
        with self.assertRaises(ArcimotoArgumentError):
            authorities_functions.factory_pin_generate(None)

    def test_factory_pin_generate_error_user_unauthorized(self):
        with self.assertRaises(ArcimotoPermissionError):
            authorities_functions.factory_pin_generate(self.vin, False)


@arcimoto.runtime.handler
def test_factory_pin_generate():
    return arcimoto.tests.handle_test_result(unittest.TextTestRunner().run(
        unittest.TestLoader().loadTestsFromTestCase(FactoryPinGenerateTestCase)
    ))


lambda_handler = test_factory_pin_generate
