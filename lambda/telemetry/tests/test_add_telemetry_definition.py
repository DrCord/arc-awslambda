import logging
import unittest


from arcimoto.exceptions import *
import arcimoto.runtime
import arcimoto.tests
import telemetry_functions

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class AddTelemetryDefinitionTestCase(unittest.TestCase):
    # doesn't do anything except in prod, only logs that it can only run in prod in dev/staging

    metrics = {
        "metrics": {
            "woke_status": {
                "type": "bool",
                "scale": None,
                "address": 257,
                "byte_list": [
                    {
                        "byte_num": 0,
                        "start_bit": 1,
                        "num_bits": 1
                    }
                ],
                "default": 0
            },
            "soc": {
                "type": "float",
                "scale": 2,
                "address": 1024,
                "byte_list": [
                    {
                        "byte_num": 0,
                        "start_bit": 0,
                        "num_bits": 8
                    }
                ],
                "default": 0
            },
            "speed": {
                "type": "float",
                "scale": 10,
                "address": 268,
                "byte_list": [
                    {
                        "byte_num": 0,
                        "start_bit": 0,
                        "num_bits": 8
                    },
                    {
                        "byte_num": 1,
                        "start_bit": 0,
                        "num_bits": 8
                    }
                ],
                "default": 0
            },
            "steering_angle": {
                "type": "int",
                "scale": None,
                "address": 268,
                "byte_list": [
                    {
                        "byte_num": 2,
                        "start_bit": 0,
                        "num_bits": 8
                    },
                    {
                        "byte_num": 3,
                        "start_bit": 0,
                        "num_bits": 8
                    }
                ],
                "default": 0
            },
            "odometer": {
                "type": "float",
                "scale": 100,
                "address": 268,
                "byte_list": [
                    {
                        "byte_num": 6,
                        "start_bit": 0,
                        "num_bits": 8
                    },
                    {
                        "byte_num": 7,
                        "start_bit": 0,
                        "num_bits": 8
                    },
                    {
                        "byte_num": 4,
                        "start_bit": 0,
                        "num_bits": 8
                    },
                    {
                        "byte_num": 5,
                        "start_bit": 0,
                        "num_bits": 8
                    }
                ],
                "default": 0
            },
            "controller_1_motor_temperature": {
                "type": "int",
                "scale": None,
                "address": 267,
                "byte_list": [
                    {
                        "byte_num": 0,
                        "start_bit": 0,
                        "num_bits": 8
                    }
                ],
                "default": 0
            },
            "controller_2_motor_temperature": {
                "type": "int",
                "scale": None,
                "address": 267,
                "byte_list": [
                    {
                        "byte_num": 1,
                        "start_bit": 0,
                        "num_bits": 8
                    }
                ],
                "default": 0
            },
            "controller_1_inverter_temperature": {
                "type": "int",
                "scale": None,
                "address": 267,
                "byte_list": [
                    {
                        "byte_num": 2,
                        "start_bit": 0,
                        "num_bits": 8
                    }
                ],
                "default": 0
            },
            "controller_2_inverter_temperature": {
                "type": "int",
                "scale": None,
                "address": 267,
                "byte_list": [
                    {
                        "byte_num": 3,
                        "start_bit": 0,
                        "num_bits": 8
                    }
                ],
                "default": 0
            },
            "controller_1_fault_level": {
                "type": "int",
                "scale": None,
                "address": 267,
                "byte_list": [
                    {
                        "byte_num": 4,
                        "start_bit": 0,
                        "num_bits": 8
                    }
                ],
                "default": 0
            },
            "controller_1_fault_code": {
                "type": "int",
                "scale": None,
                "address": 267,
                "byte_list": [
                    {
                        "byte_num": 5,
                        "start_bit": 0,
                        "num_bits": 8
                    }
                ],
                "default": 0
            },
            "controller_2_fault_level": {
                "type": "int",
                "scale": None,
                "address": 267,
                "byte_list": [
                    {
                        "byte_num": 6,
                        "start_bit": 0,
                        "num_bits": 8
                    }
                ],
                "default": 0
            },
            "controller_2_fault_code": {
                "type": "int",
                "scale": None,
                "address": 267,
                "byte_list": [
                    {
                        "byte_num": 7,
                        "start_bit": 0,
                        "num_bits": 8
                    }
                ],
                "default": 0
            }
        }
    }

    # test errors
    def test_add_telemetry_definition_error_wrong_environment(self):
        with self.assertRaises(ArcimotoException):
            telemetry_functions.add_telemetry_definition(self.metrics)

    def test_add_telemetry_definition_error_input_None_metrics(self):
        with self.assertRaises(ArcimotoArgumentError):
            telemetry_functions.add_telemetry_definition(None)

    def test_add_telemetry_definition_error_input_invalid_type_metrics(self):
        with self.assertRaises(ArcimotoArgumentError):
            telemetry_functions.add_telemetry_definition('not a dictionary')

    def test_add_telemetry_definition_error_input_invalid_empty_metrics(self):
        with self.assertRaises(ArcimotoArgumentError):
            telemetry_functions.add_telemetry_definition({})

    def test_add_telemetry_definition_error_user_unauthorized(self):
        with self.assertRaises(ArcimotoPermissionError):
            telemetry_functions.add_telemetry_definition(self.metrics, False)


@arcimoto.runtime.handler
def test_add_telemetry_definition():
    return arcimoto.tests.handle_test_result(unittest.TextTestRunner().run(
        unittest.TestLoader().loadTestsFromTestCase(AddTelemetryDefinitionTestCase)
    ))


lambda_handler = test_add_telemetry_definition
