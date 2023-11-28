import logging
import unittest

from arcimoto.exceptions import *
import arcimoto.runtime
import arcimoto.tests
import utility_functions

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class UtilityEmailAlertErrorTestCase(unittest.TestCase):

    args = {
        'Records': [
            {
                'EventSource': 'aws:sns',
                'EventVersion': '1.0',
                'EventSubscriptionArn': 'arn:aws:sns:us-west-2:511596272857:telematics_errors_dev:4d4ccb3e-d398-4566-80a5-b2e9e8c214d9',
                'Sns': {
                    'Type': 'Notification',
                    'MessageId': 'dbbd6d95-e2cf-511f-9442-377fc7a9e453',
                    'TopicArn': 'arn:aws:sns:us-west-2:511596272857:telematics_errors_dev',
                    'Subject': None,
                    'Message': '{"message": "non-JSON message\\n\\nThis message is non-JSON from unit tests", "source_type": "lambda", "source": "utility_email_alert_error:dev", "severity": "UNIT TEST", "data": {}}',
                    'Timestamp': '2022-05-02T18:29:58.992Z',
                    'SignatureVersion': '1',
                    'Signature': 'YQ6abNWqyHHGcu42o0/ovT+XpcD7oDGb9lR8PMmNItrf5Pmv3jSR8i20ImQtiyff538AtIqQ7+5YHMUwE+i3ZA3XfBjp+MGRJDWbDWpDLHtZnfdV0aoFUj2//sitOcCGbH/0h9KgunourKfVR9Cb7RBWsvysJw0VtsB3YbHEL5Kfdz/uO7e3g4MTMicYShCSFymNzKpesDFGHlpVZBvD8jxyeB60cd6SlbJjgx59h0KMsCh8i4f4TeUgnwZly2zc3vIVXPhR9Ab27yNv9nj3xmoXme4euORAeygvlYbMNmyvT4di1i1tLHW+DbUBPxlwiBn1J/yPFwCy2+8tovk9/A==',
                    'SigningCertUrl': 'https://sns.us-west-2.amazonaws.com/SimpleNotificationService-7ff5318490ec183fbaddaa2a969abfda.pem',
                    'UnsubscribeUrl': 'https://sns.us-west-2.amazonaws.com/?Action=Unsubscribe&SubscriptionArn=arn:aws:sns:us-west-2:511596272857:telematics_errors_dev:4d4ccb3e-d398-4566-80a5-b2e9e8c214d9',
                    'MessageAttributes': {}
                }
            },
            {
                'EventSource': 'aws:sns',
                'EventVersion': '1.0',
                'EventSubscriptionArn': 'arn:aws:sns:us-west-2:511596272857:telematics_errors_dev:4d4ccb3e-d398-4566-80a5-b2e9e8c214d9',
                'Sns': {
                    'Type': 'Notification',
                    'MessageId': 'dbbd6d95-e2cf-511f-9442-377fc7a9e453',
                    'TopicArn': 'arn:aws:sns:us-west-2:511596272857:telematics_errors_dev',
                    'Subject': None,
                    'Message': {
                        "message": "JSON message. This message is JSON from unit tests",
                        "source_type": "lambda",
                        "source": "utility_email_alert_error:dev",
                        "severity": "UNIT TEST",
                        "data": {}
                    },
                    'Timestamp': '2022-05-02T18:29:58.992Z',
                    'SignatureVersion': '1',
                    'Signature': 'YQ6abNWqyHHGcu42o0/ovT+XpcD7oDGb9lR8PMmNItrf5Pmv3jSR8i20ImQtiyff538AtIqQ7+5YHMUwE+i3ZA3XfBjp+MGRJDWbDWpDLHtZnfdV0aoFUj2//sitOcCGbH/0h9KgunourKfVR9Cb7RBWsvysJw0VtsB3YbHEL5Kfdz/uO7e3g4MTMicYShCSFymNzKpesDFGHlpVZBvD8jxyeB60cd6SlbJjgx59h0KMsCh8i4f4TeUgnwZly2zc3vIVXPhR9Ab27yNv9nj3xmoXme4euORAeygvlYbMNmyvT4di1i1tLHW+DbUBPxlwiBn1J/yPFwCy2+8tovk9/A==',
                    'SigningCertUrl': 'https://sns.us-west-2.amazonaws.com/SimpleNotificationService-7ff5318490ec183fbaddaa2a969abfda.pem',
                    'UnsubscribeUrl': 'https://sns.us-west-2.amazonaws.com/?Action=Unsubscribe&SubscriptionArn=arn:aws:sns:us-west-2:511596272857:telematics_errors_dev:4d4ccb3e-d398-4566-80a5-b2e9e8c214d9',
                    'MessageAttributes': {}
                }
            }
        ]
    }

    def test_email_alert_error_success(self):
        self.assertIsInstance(utility_functions.email_alert_error(self.args), dict)


@arcimoto.runtime.handler
def test_email_alert_error():
    return arcimoto.tests.handle_test_result(unittest.TextTestRunner().run(
        unittest.TestLoader().loadTestsFromTestCase(UtilityEmailAlertErrorTestCase)
    ))


lambda_handler = test_email_alert_error
