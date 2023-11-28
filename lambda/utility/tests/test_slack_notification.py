import logging
import json
import unittest
import copy

from arcimoto.exceptions import *
import arcimoto.runtime
import arcimoto.tests
import utility_functions

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class SlackNotificationTestCase(unittest.TestCase):

    args_json = {
        "Records": [
            {
                "Sns": {
                    "Subject": "set_db_telemetry_alarm testing subject",
                    "Message": {
                        "AlarmName": "Telemetry rate DEV-TEST-7F7ATR312LER00015 - UNIT TEST",
                        "AlarmDescription": "Telemetry rate above flip threshold for VIN DEV-TEST-7F7ATR312LER00015 - UNIT TEST",
                        "AWSAccountId": "511596272857",
                        "AlarmConfigurationUpdatedTimestamp": "2021-05-20T15:39:17.692+0000",
                        "NewStateValue": "ALARM",
                        "NewStateReason": "Threshold Crossed: 5 datapoints were greater than the threshold (2.0). The most recent datapoints which crossed the threshold: [7.0 (21/04/22 20:24:00), 4.0 (21/04/22 20:19:00), 5.0 (21/04/22 20:14:00), 3.0 (21/04/22 20:09:00), 4.0 (21/04/22 20:04:00)].",
                        "StateChangeTime": "2022-04-21T20:29:41.411+0000",
                        "Region": "US West (Oregon)",
                        "AlarmArn": "arn:aws:cloudwatch:us-west-2:511596272857:alarm:Telemetry rate DEV-7F7ATR312LER00015",
                        "OldStateValue": "OK",
                        "OKActions": [],
                        "AlarmActions": [
                            "arn:aws:sns:us-west-2:511596272857:flip_telemetry_alarm_topic_dev"
                        ],
                        "InsufficientDataActions": [],
                        "Trigger": {
                            "MetricName": "Telemetry Message Rate for VIN DEV-7F7ATR312LER00015",
                            "Namespace": "LogMetrics",
                            "StatisticType": "Statistic",
                            "Statistic": "SUM",
                            "Unit": None,
                            "Dimensions": [],
                            "Period": 300,
                            "EvaluationPeriods": 5,
                            "ComparisonOperator": "GreaterThanThreshold",
                            "Threshold": 2.0,
                            "TreatMissingData": "",
                            "EvaluateLowSampleCountPercentile": ""
                        }
                    }
                }
            },
            {
                "Sns": {
                    "Subject": "set_db_telemetry_alarm testing subject",
                    "Message": {
                        "AlarmName": "EC2 - memory percent used - STAGE-InfluxDB - UNIT TEST",
                        "AlarmDescription": "STAGE-InfluxDB EC2 Memory Percent Used outside of 2 sigma band - UNIT TEST",
                        "AWSAccountId": "511596272857",
                        "NewStateValue": "ALARM",
                        "NewStateReason": "Thresholds Crossed: 2 out of the last 2 datapoints [28.244242980188464 (22/11/19 00:57:00), 27.035814838199848 (22/11/19 00:52:00)] were less than the lower thresholds [31.723549397187316, 31.317673764600034] or greater than the upper thresholds [33.09242087209403, 32.68864166862828] (minimum 2 datapoints for OK -> ALARM transition).",
                        "StateChangeTime": "2019-11-22T01:02:17.570+0000",
                        "Region": "US West (Oregon)",
                        "OldStateValue": "OK",
                        "Trigger": {
                            "Period": 300,
                            "EvaluationPeriods": 2,
                            "ComparisonOperator": "LessThanLowerOrGreaterThanUpperThreshold",
                            "ThresholdMetricId": "ad1",
                            "TreatMissingData": "- TreatMissingData:                    missing",
                            "EvaluateLowSampleCountPercentile": "",
                            "Metrics": [
                                {
                                    "Id": "m1",
                                    "MetricStat": {
                                        "Metric": {
                                            "Dimensions": [
                                                {
                                                    "value": "i-046d48b26d0fd82ca",
                                                    "name": "InstanceId"
                                                },
                                                {
                                                    "value": "ami-04b762b4289fba92b",
                                                    "name": "ImageId"
                                                },
                                                {
                                                    "value": "t2.micro",
                                                    "name": "InstanceType"
                                                }
                                            ],
                                            "MetricName": "mem_used_percent",
                                            "Namespace": "CWAgent"
                                        },
                                        "Period": 300,
                                        "Stat": "Average"
                                    },
                                    "ReturnData": True
                                },
                                {
                                    "Expression": "ANOMALY_DETECTION_BAND(m1, 0.2)",
                                    "Id": "ad1",
                                    "Label": "mem_used_percent (expected)",
                                    "ReturnData": True
                                }
                            ]
                        }
                    }
                }
            }
        ]
    }
    args_string_non_json = {
        "Records": [
            {
                "Sns": {
                    "Subject": "non-JSON message",
                    "Message": "This message is non-JSON"
                }
            },
            {
                "Sns": {
                    "Subject": "JSON decodable message",
                    "Message": "{\"AlarmName\": \"This message is JSON\", \"AlarmDescription\":\"Test description\"}"
                }
            }
        ]
    }
    args_string_json = {
        "Records": [
            {
                "Sns": {
                    "Subject": "JSON decodable message",
                    "Message": "{\"AlarmName\": \"This message is JSON\", \"AlarmDescription\":\"Test description\"}"
                }
            }
        ]
    }
    args_aws_health_message = {
        "Records": [
            {
                "Sns": {
                    "Subject": "AWS Health Unit Test Message",
                    "Message": {
                        "version": "0",
                        "id": "78cf314f-47ba-4d9b-7c24-a3345b103512",
                        "detail-type": "AWS Health Event",
                        "source": "aws.health",
                        "account": "511596272857",
                        "time": "2022-05-10T06:00:54Z",
                        "region": "us-west-2",
                        "resources": [
                            "vpn-0d2aca25695801ce2"
                        ],
                        "detail": {
                            "eventArn": "arn:aws:health:us-west-2::event/VPN/AWS_VPN_REDUNDANCY_LOSS/AWS_VPN_REDUNDANCY_LOSS-1652162668164-6104858-PDX",
                            "service": "VPN",
                            "eventTypeCode": "AWS_VPN_REDUNDANCY_LOSS",
                            "eventTypeCategory": "accountNotification",
                            "startTime": "Tue, 10 May 2022 06:00:54 GMT",
                            "eventDescription": [
                                {
                                    "language": "en_US",
                                    "latestDescription": "This is a unit test generated message"
                                }
                            ],
                            "affectedEntities": [
                                {
                                    "entityValue": "vpn-0d2aca25695801ce2"
                                }
                            ]
                        }
                    }
                }
            },
            {
                "Sns": {
                    "Subject": "AWS Health Unit Test Message 2",
                    "Message": {
                        "version": "0",
                        "id": "78cf314f-47ba-4d9b-7c24-a3345b103512",
                        "detail-type": "AWS Health Event",
                        "source": "aws.health",
                        "account": "511596272857",
                        "time": "2022-05-10T06:00:54Z",
                        "region": "us-west-2",
                        "resources": [
                            "vpn-0d2aca25695801ce2"
                        ],
                        "detail": {
                            "eventArn": "arn:aws:health:us-west-2::event/ACM/",
                            "service": "ACM",
                            "eventTypeCode": "AWS_ACM_RENEWAL_STATE_CHANGE",
                            "eventTypeCategory": "accountNotification",
                            "startTime": "Tue, 10 May 2022 06:00:54 GMT",
                            "eventDescription": [
                                {
                                    "language": "en_US",
                                    "latestDescription": "This is a unit test generated message"
                                }
                            ],
                            "affectedEntities": [
                                {
                                    "entityValue": "vpn-0d2aca25695801ce2"
                                }
                            ]
                        }
                    }
                }
            }
        ]
    }

    args_no_cloudwatch_alarm_info = ''

    def test_slack_notification_success_json(self):
        self.assertIsInstance(utility_functions.slack_notification(self.args_json), dict)

    def test_slack_notification_success_non_json_string(self):
        self.assertIsInstance(utility_functions.slack_notification(self.args_string_non_json), dict)

    def test_slack_notification_success_json_string(self):
        self.assertIsInstance(utility_functions.slack_notification(self.args_string_json), dict)

    def test_slack_notification_success_aws_health_message(self):
        self.assertIsInstance(utility_functions.slack_notification(self.args_aws_health_message), dict)

    # test errors
    def test_slack_notification_error_no_cloudwatch_alarm_info(self):
        args = copy.deepcopy(self.args_aws_health_message)
        args['Records'][0]['Sns']['Subject'] = 'Non Alarm/Health Message'
        args['Records'][0]['Sns']['Message']['source'] = None
        with self.assertRaises(ArcimotoAlertException):
            utility_functions.slack_notification(args)


@arcimoto.runtime.handler
def test_slack_notification():
    return arcimoto.tests.handle_test_result(unittest.TextTestRunner().run(
        unittest.TestLoader().loadTestsFromTestCase(SlackNotificationTestCase)
    ))


lambda_handler = test_slack_notification
