from copy import deepcopy
import logging
import unittest

from arcimoto.exceptions import *
import arcimoto.runtime
import arcimoto.tests
import unit_test_functions

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class UnitTestLambdasTestsReportTestCase(unittest.TestCase):

    args = {
        'lambdas_tests_results': [
            {
                "bundle_name": "alarms",
                "lambdas": [
                    "monitor_influxdb_backup",
                    "provision_telemetry_alarm",
                    "set_db_telemetry_alarm",
                    "unprovision_telemetry_alarm",
                    "unset_db_telemetry_alarm"
                ],
                "lambda_tests": [
                    {
                        "lambda_name": "monitor_influxdb_backup",
                        "lambda_tests": {
                            "lambda_tests": {
                                "lambda_tests": []
                            }
                        },
                        "test_results": {
                            "test_results": {
                                "lambda_name": "monitor_influxdb_backup",
                                "test_results": [
                                    {
                                        "message": "The lambda monitor_influxdb_backup does not have any tests",
                                        "status": "NOTESTS"
                                    }
                                ]
                            }
                        }
                    },
                    {
                        "lambda_name": "provision_telemetry_alarm",
                        "lambda_tests": {
                            "lambda_tests": {
                                "lambda_tests": []
                            }
                        },
                        "test_results": {
                            "test_results": {
                                "lambda_name": "provision_telemetry_alarm",
                                "test_results": [
                                    {
                                        "message": "The lambda provision_telemetry_alarm does not have any tests",
                                        "status": "NOTESTS"
                                    }
                                ]
                            }
                        }
                    },
                    {
                        "lambda_name": "set_db_telemetry_alarm",
                        "lambda_tests": {
                            "lambda_tests": {
                                "lambda_tests": []
                            }
                        },
                        "test_results": {
                            "test_results": {
                                "lambda_name": "set_db_telemetry_alarm",
                                "test_results": [
                                    {
                                        "message": "The lambda set_db_telemetry_alarm does not have any tests",
                                        "status": "NOTESTS"
                                    }
                                ]
                            }
                        }
                    },
                    {
                        "lambda_name": "unprovision_telemetry_alarm",
                        "lambda_tests": {
                            "lambda_tests": {
                                "lambda_tests": []
                            }
                        },
                        "test_results": {
                            "test_results": {
                                "lambda_name": "unprovision_telemetry_alarm",
                                "test_results": [
                                    {
                                        "message": "The lambda unprovision_telemetry_alarm does not have any tests",
                                        "status": "NOTESTS"
                                    }
                                ]
                            }
                        }
                    },
                    {
                        "lambda_name": "unset_db_telemetry_alarm",
                        "lambda_tests": {
                            "lambda_tests": {
                                "lambda_tests": []
                            }
                        },
                        "test_results": {
                            "test_results": {
                                "lambda_name": "unset_db_telemetry_alarm",
                                "test_results": [
                                    {
                                        "message": "The lambda unset_db_telemetry_alarm does not have any tests",
                                        "status": "NOTESTS"
                                    }
                                ]
                            }
                        }
                    }
                ]
            },
            {
                "bundle_name": "authorities",
                "lambdas": [
                    "authkey_vehicle_get",
                    "create_authority",
                    "delete_authority",
                    "factory_pin_generate",
                    "get_authority",
                    "get_trusted_keys",
                    "list_authorities",
                    "list_vehicles",
                    "provision_vehicle_authority",
                    "rekey_authority",
                    "sign_vehicle_token",
                    "unprovision_vehicle_arcimoto_authority",
                    "unprovision_vehicle_authority"
                ],
                "lambda_tests": [
                    {
                        "lambda_name": "authkey_vehicle_get",
                        "lambda_tests": {
                            "lambda_tests": {
                                "lambda_tests": [
                                    "test_authkey_vehicle_get"
                                ]
                            }
                        },
                        "test_results": {
                            "test_results": {
                                "lambda_name": "authkey_vehicle_get",
                                "test_results": [
                                    {
                                        "message": "4 tests run",
                                        "status": "SUCCESS",
                                        "lambda_test_name": "test_authkey_vehicle_get"
                                    }
                                ]
                            }
                        }
                    },
                    {
                        "lambda_name": "create_authority",
                        "lambda_tests": {
                            "lambda_tests": {
                                "lambda_tests": [
                                    "test_create_authority"
                                ]
                            }
                        },
                        "test_results": {
                            "test_results": {
                                "lambda_name": "create_authority",
                                "test_results": [
                                    {
                                        "message": "4 tests run",
                                        "status": "SUCCESS",
                                        "lambda_test_name": "test_create_authority"
                                    }
                                ]
                            }
                        }
                    },
                    {
                        "lambda_name": "delete_authority",
                        "lambda_tests": {
                            "lambda_tests": {
                                "lambda_tests": [
                                    "test_delete_authority"
                                ]
                            }
                        },
                        "test_results": {
                            "test_results": {
                                "lambda_name": "delete_authority",
                                "test_results": [
                                    {
                                        "message": "6 tests run",
                                        "status": "SUCCESS",
                                        "lambda_test_name": "test_delete_authority"
                                    }
                                ]
                            }
                        }
                    },
                    {
                        "lambda_name": "factory_pin_generate",
                        "lambda_tests": {
                            "lambda_tests": {
                                "lambda_tests": [
                                    "test_factory_pin_generate"
                                ]
                            }
                        },
                        "test_results": {
                            "test_results": {
                                "lambda_name": "factory_pin_generate",
                                "test_results": [
                                    {
                                        "message": "3 tests run",
                                        "status": "SUCCESS",
                                        "lambda_test_name": "test_factory_pin_generate"
                                    }
                                ]
                            }
                        }
                    },
                    {
                        "lambda_name": "get_authority",
                        "lambda_tests": {
                            "lambda_tests": {
                                "lambda_tests": [
                                    "test_get_authority"
                                ]
                            }
                        },
                        "test_results": {
                            "test_results": {
                                "lambda_name": "get_authority",
                                "test_results": [
                                    {
                                        "message": "4 tests run",
                                        "status": "SUCCESS",
                                        "lambda_test_name": "test_get_authority"
                                    }
                                ]
                            }
                        }
                    },
                    {
                        "lambda_name": "get_trusted_keys",
                        "lambda_tests": {
                            "lambda_tests": {
                                "lambda_tests": [
                                    "test_get_trusted_keys"
                                ]
                            }
                        },
                        "test_results": {
                            "test_results": {
                                "lambda_name": "get_trusted_keys",
                                "test_results": [
                                    {
                                        "message": "2 tests run",
                                        "status": "SUCCESS",
                                        "lambda_test_name": "test_get_trusted_keys"
                                    }
                                ]
                            }
                        }
                    },
                    {
                        "lambda_name": "list_authorities",
                        "lambda_tests": {
                            "lambda_tests": {
                                "lambda_tests": [
                                    "test_list_authorities"
                                ]
                            }
                        },
                        "test_results": {
                            "test_results": {
                                "lambda_name": "list_authorities",
                                "test_results": [
                                    {
                                        "message": "6 tests run",
                                        "status": "SUCCESS",
                                        "lambda_test_name": "test_list_authorities"
                                    }
                                ]
                            }
                        }
                    },
                    {
                        "lambda_name": "list_vehicles",
                        "lambda_tests": {
                            "lambda_tests": {
                                "lambda_tests": [
                                    "test_list_vehicles"
                                ]
                            }
                        },
                        "test_results": {
                            "test_results": {
                                "lambda_name": "list_vehicles",
                                "test_results": [
                                    {
                                        "message": "3 tests run",
                                        "status": "SUCCESS",
                                        "lambda_test_name": "test_list_vehicles"
                                    }
                                ]
                            }
                        }
                    },
                    {
                        "lambda_name": "provision_vehicle_authority",
                        "lambda_tests": {
                            "lambda_tests": {
                                "lambda_tests": [
                                    "test_provision_vehicle_authority"
                                ]
                            }
                        },
                        "test_results": {
                            "test_results": {
                                "lambda_name": "provision_vehicle_authority",
                                "test_results": [
                                    {
                                        "message": "6 tests run",
                                        "status": "SUCCESS",
                                        "lambda_test_name": "test_provision_vehicle_authority"
                                    }
                                ]
                            }
                        }
                    },
                    {
                        "lambda_name": "rekey_authority",
                        "lambda_tests": {
                            "lambda_tests": {
                                "lambda_tests": [
                                    "test_rekey_authority"
                                ]
                            }
                        },
                        "test_results": {
                            "test_results": {
                                "lambda_name": "rekey_authority",
                                "test_results": [
                                    {
                                        "message": "3 tests run",
                                        "status": "SUCCESS",
                                        "lambda_test_name": "test_rekey_authority"
                                    }
                                ]
                            }
                        }
                    },
                    {
                        "lambda_name": "sign_vehicle_token",
                        "lambda_tests": {
                            "lambda_tests": {
                                "lambda_tests": [
                                    "test_sign_vehicle_token"
                                ]
                            }
                        },
                        "test_results": {
                            "test_results": {
                                "lambda_name": "sign_vehicle_token",
                                "test_results": [
                                    {
                                        "message": "8 tests run",
                                        "status": "SUCCESS",
                                        "lambda_test_name": "test_sign_vehicle_token"
                                    }
                                ]
                            }
                        }
                    },
                    {
                        "lambda_name": "unprovision_vehicle_arcimoto_authority",
                        "lambda_tests": {
                            "lambda_tests": {
                                "lambda_tests": [
                                    "test_unprovision_vehicle_arcimoto_authority"
                                ]
                            }
                        },
                        "test_results": {
                            "test_results": {
                                "lambda_name": "unprovision_vehicle_arcimoto_authority",
                                "test_results": [
                                    {
                                        "message": "3 tests run",
                                        "status": "SUCCESS",
                                        "lambda_test_name": "test_unprovision_vehicle_arcimoto_authority"
                                    }
                                ]
                            }
                        }
                    },
                    {
                        "lambda_name": "unprovision_vehicle_authority",
                        "lambda_tests": {
                            "lambda_tests": {
                                "lambda_tests": [
                                    "test_unprovision_vehicle_authority"
                                ]
                            }
                        },
                        "test_results": {
                            "test_results": {
                                "lambda_name": "unprovision_vehicle_authority",
                                "test_results": [
                                    {
                                        "message": "8 tests run",
                                        "status": "SUCCESS",
                                        "lambda_test_name": "test_unprovision_vehicle_authority"
                                    }
                                ]
                            }
                        }
                    }
                ]
            },
            {
                "bundle_name": "backfill",
                "lambdas": [
                    "backfill_ingest_request",
                    "backfill_notify_complete",
                    "backfill_notify_failed",
                    "backfill_s3_delete_file",
                    "backfill_s3_load_file",
                    "backfill_s3_presigned_url_generate",
                    "backfill_state_machine_start"
                ],
                "lambda_tests": [
                    {
                        "lambda_name": "backfill_ingest_request",
                        "lambda_tests": {
                            "lambda_tests": {
                                "lambda_tests": [
                                    "test_backfill_ingest_request"
                                ]
                            }
                        },
                        "test_results": {
                            "test_results": {
                                "lambda_name": "backfill_ingest_request",
                                "test_results": [
                                    {
                                        "message": "6 tests run",
                                        "status": "SUCCESS",
                                        "lambda_test_name": "test_backfill_ingest_request"
                                    }
                                ]
                            }
                        }
                    },
                    {
                        "lambda_name": "backfill_notify_complete",
                        "lambda_tests": {
                            "lambda_tests": {
                                "lambda_tests": [
                                    "test_backfill_notify_complete"
                                ]
                            }
                        },
                        "test_results": {
                            "test_results": {
                                "lambda_name": "backfill_notify_complete",
                                "test_results": [
                                    {
                                        "message": "7 tests run",
                                        "status": "SUCCESS",
                                        "lambda_test_name": "test_backfill_notify_complete"
                                    }
                                ]
                            }
                        }
                    },
                    {
                        "lambda_name": "backfill_notify_failed",
                        "lambda_tests": {
                            "lambda_tests": {
                                "lambda_tests": [
                                    "test_backfill_notify_failed"
                                ]
                            }
                        },
                        "test_results": {
                            "test_results": {
                                "lambda_name": "backfill_notify_failed",
                                "test_results": [
                                    {
                                        "message": "7 tests run",
                                        "status": "SUCCESS",
                                        "lambda_test_name": "test_backfill_notify_failed"
                                    }
                                ]
                            }
                        }
                    },
                    {
                        "lambda_name": "backfill_s3_delete_file",
                        "lambda_tests": {
                            "lambda_tests": {
                                "lambda_tests": [
                                    "test_backfill_s3_delete_file"
                                ]
                            }
                        },
                        "test_results": {
                            "test_results": {
                                "lambda_name": "backfill_s3_delete_file",
                                "test_results": [
                                    {
                                        "message": "3 tests run",
                                        "status": "SUCCESS",
                                        "lambda_test_name": "test_backfill_s3_delete_file"
                                    }
                                ]
                            }
                        }
                    },
                    {
                        "lambda_name": "backfill_s3_load_file",
                        "lambda_tests": {
                            "lambda_tests": {
                                "lambda_tests": [
                                    "test_backfill_s3_load_file"
                                ]
                            }
                        },
                        "test_results": {
                            "test_results": {
                                "lambda_name": "backfill_s3_load_file",
                                "test_results": [
                                    {
                                        "message": "6 tests run",
                                        "status": "SUCCESS",
                                        "lambda_test_name": "test_backfill_s3_load_file"
                                    }
                                ]
                            }
                        }
                    },
                    {
                        "lambda_name": "backfill_s3_presigned_url_generate",
                        "lambda_tests": {
                            "lambda_tests": {
                                "lambda_tests": [
                                    "test_backfill_s3_presigned_url_generate"
                                ]
                            }
                        },
                        "test_results": {
                            "test_results": {
                                "lambda_name": "backfill_s3_presigned_url_generate",
                                "test_results": [
                                    {
                                        "message": "3 tests run",
                                        "status": "SUCCESS",
                                        "lambda_test_name": "test_backfill_s3_presigned_url_generate"
                                    }
                                ]
                            }
                        }
                    },
                    {
                        "lambda_name": "backfill_state_machine_start",
                        "lambda_tests": {
                            "lambda_tests": {
                                "lambda_tests": [
                                    "test_backfill_state_machine_start"
                                ]
                            }
                        },
                        "test_results": {
                            "test_results": {
                                "lambda_name": "backfill_state_machine_start",
                                "test_results": [
                                    {
                                        "message": "7 tests run",
                                        "status": "SUCCESS",
                                        "lambda_test_name": "test_backfill_state_machine_start"
                                    }
                                ]
                            }
                        }
                    }
                ]
            }
        ],
        'message_addendum': 'Unit test test_unit_test_lambdas_tests_report message addendum'
    }

    def test_unit_test_lambdas_tests_report_success(self):
        self.assertIsInstance(unit_test_functions.unit_test_lambdas_tests_report(self.args), dict)

    # test errors
    def test_unit_test_lambda_run_tests_error_input_no_lambdas_tests_results(self):
        args = deepcopy(self.args)
        del args['lambdas_tests_results']
        with self.assertRaises(ArcimotoArgumentError):
            unit_test_functions.unit_test_lambda_run_tests(args)

    def test_unit_test_lambda_run_tests_error_input_null_lambdas_tests_results(self):
        args = deepcopy(self.args)
        args['lambdas_tests_results'] = None
        with self.assertRaises(ArcimotoArgumentError):
            unit_test_functions.unit_test_lambda_run_tests(args)

    def test_unit_test_lambda_run_tests_error_input_invalid_type_lambdas_tests_results(self):
        args = deepcopy(self.args)
        args['lambdas_tests_results'] = 'not a list'
        with self.assertRaises(ArcimotoArgumentError):
            unit_test_functions.unit_test_lambda_run_tests(args)

    def test_unit_test_lambda_run_tests_error_input_invalid_type_message_addendum(self):
        args = deepcopy(self.args)
        args['message_addendum'] = 1
        with self.assertRaises(ArcimotoArgumentError):
            unit_test_functions.unit_test_lambda_run_tests(args)

    def test_unit_test_lambda_run_tests_error_input_no_lambda_name_in_test_result(self):
        args = deepcopy(self.args)
        del args['lambdas_tests_results'][0]['lambda_tests'][0]['lambda_name']
        with self.assertRaises(ArcimotoArgumentError):
            unit_test_functions.unit_test_lambda_run_tests(args)

    def test_unit_test_lambda_run_tests_error_input_unable_to_parse_status_in_test_result(self):
        args = deepcopy(self.args)
        args['lambdas_tests_results'][0]['lambda_tests'][0]['test_results']['test_results']['test_results'][0]['status'] = 'not a allowed status!'
        with self.assertRaises(ArcimotoArgumentError):
            unit_test_functions.unit_test_lambda_run_tests(args)


@arcimoto.runtime.handler
def test_unit_test_lambdas_tests_report():
    return arcimoto.tests.handle_test_result(unittest.TextTestRunner().run(
        unittest.TestLoader().loadTestsFromTestCase(UnitTestLambdasTestsReportTestCase)
    ))


lambda_handler = test_unit_test_lambdas_tests_report
