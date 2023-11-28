import logging
import json

from arcimoto.exceptions import *
import arcimoto.runtime
import arcimoto.note

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

arcimoto.args.register({
    'lambdas_tests_results': {
        'type': 'list',
        'required': True
    },
    'message_addendum': {
        'type': 'string',
        'default': None,
        'nullable': True
    }
})


@arcimoto.runtime.handler
def unit_test_lambdas_tests_report(lambdas_tests_results, message_addendum):
    global logger

    failure = []
    failure_data = {}
    no_tests = []
    success = []

    for lambdas_tests_data in lambdas_tests_results:
        lambdas_tests_results = lambdas_tests_data.get('lambda_tests')
        for lambda_tests_data in lambdas_tests_results:
            lambda_name = lambda_tests_data.get('lambda_name', None)
            if lambda_name is None:
                raise ArcimotoAlertException(f'Unable to get lambda name from tests data: {lambda_tests_data}')

            lambda_tests_result = lambda_tests_data.get('test_results', {}).get('test_results', {}).get('test_results', [])
            for lambda_test_result in lambda_tests_result:
                lambda_test_name = lambda_test_result.get('lambda_test_name', None)
                logger.info(f'Function {lambda_name} test {lambda_test_name} result: {lambda_test_result}')

                result_status = lambda_test_result.get('status', None)
                if result_status is None:
                    # tests had an exception that prevented completion so status unavailable
                    result_status = 'FAILURE: ERROR'
                result_status = result_status.lower()

                # put in buckets
                if 'failure' in result_status:
                    failure.append(lambda_name)
                    failure_data[lambda_name] = lambda_tests_result
                elif 'success' in result_status:
                    success.append(lambda_name)
                elif 'notests' in result_status:
                    no_tests.append(lambda_name)
                else:
                    raise ArcimotoAlertException(f'Unable to parse test results for status {result_status}: {lambda_tests_result}')

    output = {
        'failure': sorted(failure),
        'failure_data': failure_data,
        'no_tests': sorted(no_tests),
        'success': sorted(success)
    }

    # notification - failures
    if len(failure):
        send_notification('Failures', message_addendum, output.get('failure'), 'ERROR')

    # notification - no tests
    if len(no_tests):
        send_notification('No Tests', message_addendum, output.get('no_tests'), 'WARNING')

    # notification - successes
    if len(success):
        send_notification('Successes', message_addendum, output.get('success'))

    return output


def send_notification(event, message_addendum, event_data, severity='INFO'):
    try:
        msg_lines = [
            'Lambda Tests Suite',
            event
        ]
        if message_addendum is not None:
            msg_lines.append(message_addendum)

        msg = '\n'.join(msg_lines) + f'\n\n' + "\n".join(event_data)

        arcimoto.note.Notification(
            message=msg,
            source='Lambdas-Test',
            source_type='state_machine',
            severity=severity
        )
    except Exception as e:
        raise ArcimotoAlertException(f'Failed to send lambda test suites {event} notification: {e}')


lambda_handler = unit_test_lambdas_tests_report
