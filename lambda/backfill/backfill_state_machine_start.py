import logging
import json
import base64
import boto3
from datetime import datetime

from arcimoto.exceptions import *
import arcimoto.runtime
import arcimoto.args

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

arcimoto.args.register({
    'vin': {
        'type': 'string',
        'required': True
    },
    'file_name': {
        'type': 'string',
        'required': True
    },
    'file_length': {
        'type': 'integer',
        'required': True
    }
})

STATE_MACHINE_ARN = 'arn:aws:states:us-west-2:511596272857:stateMachine:Telemetry_Backfill'
ENV = None


@arcimoto.runtime.handler
@arcimoto.user.require('telemetry.backfill.engineering')
def backfill_state_machine_start(vin, file_name, file_length):
    global logger, STATE_MACHINE_ARN, ENV

    # return email for eventual notification of completion or error in state machine
    user = arcimoto.user.current()
    user_profile = user.get_profile()

    client = boto3.client('stepfunctions')

    now = datetime.now().strftime('%Y%m%d-%H%M%S')
    ENV = arcimoto.runtime.get_env()

    state_machine_execution_name = f'bfapi_{ENV}_{vin}_{now}'
    input = {
        "input": {
            "vin": vin,
            "file_name": file_name,
            "file_length": file_length,
            "initiating_user_email": user_profile.get('email'),
            "env": ENV
        },
        "s3_load_file": {
            "Payload": {
                "next_iteration_read_byte": 0
            }
        }
    }
    state_machine_input = json.dumps(input)

    try:
        response = client.start_execution(
            stateMachineArn=STATE_MACHINE_ARN,
            name=state_machine_execution_name,
            input=state_machine_input
        )
    except Exception as e:
        raise ArcimotoServiceAlertException(e)

    http_status_code = response.get('ResponseMetadata', {}).get('HTTPStatusCode', None)

    if http_status_code == 200:
        return {
            'message': 'Success',
            'state_machine_execution_arn': response.get('executionArn', '')
        }

    return response


lambda_handler = backfill_state_machine_start
