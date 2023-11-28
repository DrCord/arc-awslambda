import logging
from botocore.exceptions import ClientError

from arcimoto.exceptions import *
import arcimoto.runtime

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

arcimoto.args.register({
    'lambda_name': {
        'type': 'string',
        'required': True,
        'empty': False
    },
    'lambda_tests': {
        'type': 'list',
        'required': True
    }
})


@arcimoto.runtime.handler
def unit_test_lambda_run_tests(lambda_name, lambda_tests):
    global logger

    test_results = []
    if len(lambda_tests) == 0:
        no_tests_msg = {
            'message': f'The lambda {lambda_name} does not have any tests',
            'status': 'NOTESTS'
        }
        test_results.append(no_tests_msg)
    else:
        for lambda_test_name in lambda_tests:
            test_result = None
            try:
                test_result = arcimoto.runtime.invoke_lambda(lambda_test_name, {})
            except ClientError as e:
                if e.response['Error']['Code'] == 'ResourceNotFoundException':
                    test_result = {
                        'message': f'ResourceNotFoundException: The lambda test {lambda_test_name} does not exist',
                        'status': 'NOTESTS'
                    }
                    logger.warn(f'ResourceNotFoundException: The lambda test {lambda_test_name} does not exist')
                else:
                    raise ArcimotoAlertException(f'ClientError: Unable to complete test {lambda_test_name} for lambda {lambda_name}: {e}')
            except Exception as e:
                raise ArcimotoAlertException(f'Unable to complete test {lambda_test_name} for lambda {lambda_name}: {e}')

            test_result['lambda_test_name'] = lambda_test_name
            test_results.append(test_result)

    return {
        'lambda_name': lambda_name,
        'test_results': test_results
    }


lambda_handler = unit_test_lambda_run_tests
