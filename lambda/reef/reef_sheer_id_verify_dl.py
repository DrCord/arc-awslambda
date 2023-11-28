import logging
import json
import urllib3
import certifi

from arcimoto.exceptions import *
import arcimoto.runtime
import arcimoto.user
import arcimoto.args
import arcimoto.db

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

arcimoto.args.register({
    'first_name': {
        'type': 'string',
        'required': True,
        'empty': False
    },
    'last_name': {
        'type': 'string',
        'required': True,
        'empty': False
    },
    'email': {
        'type': 'string',
        'required': True,
        'empty': False
    },
    'drivers_license_number': {
        'type': 'string',
        'required': True,
        'empty': False
    },
    'state': {
        'type': 'string',
        'required': True,
        'empty': False
    }
})


@arcimoto.runtime.handler
def reef_sheer_id_verify_dl(first_name, last_name, email, drivers_license_number, state):
    global logger

    BASE_URL = 'https://services.sheerid.com/rest/v2/'
    program_id_secret = arcimoto.runtime.get_secret(f'sheer_id.program_id.reef.{arcimoto.runtime.get_env()}')
    PROGRAM_ID = str(program_id_secret.get('program_id'))
    API_URL = f'{BASE_URL}verification/program/{PROGRAM_ID}/step/collectDriverLicensePersonalInfo'

    payload = {
        'firstName': first_name,
        'lastName': last_name,
        'email': email,
        'driverLicenseNumber': drivers_license_number,
        'state': state
    }
    encoded_data = json.dumps(payload).encode('utf-8')

    try:
        sheer_id_secret = arcimoto.runtime.get_secret('sheer_id.api.reef')
        api_call_headers = {
            'Authorization': 'Bearer ' + str(sheer_id_secret.get('api_key')),
            'Content-Type': 'application/json'
        }
    except Exception as e:
        raise ArcimotoREEFAlertException(f'Unable to get create headers for request: {e}') from e

    try:
        # recommended to do ssl verification for requests
        # https://urllib3.readthedocs.io/en/latest/user-guide.html#ssl
        http = urllib3.PoolManager(
            cert_reqs='CERT_REQUIRED',
            ca_certs=certifi.where()
        )
        api_call_response = http.request(
            'POST',
            API_URL,
            body=encoded_data,
            headers=api_call_headers
        )
    except Exception as e:
        raise ArcimotoREEFAlertException(f'Unable to complete POST request - error: {e}') from e

    verified = False

    try:
        json_response = json.loads(api_call_response.data.decode('utf-8'))
        if api_call_response.status == 200 and 'currentStep' in json_response:
            verified = True if json_response.get('currentStep') == 'success' else False
    except Exception as e:
        raise ArcimotoREEFAlertException(f'Unable to parse json response - error: {e}') from e

    return {
        'verified': verified,
        'verification_id': json_response.get('verificationId', None)
    }


lambda_handler = reef_sheer_id_verify_dl
