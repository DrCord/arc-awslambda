import logging
import requests

from arcimoto.exceptions import *
import arcimoto.runtime
import arcimoto.args
import arcimoto.user

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

arcimoto.args.register({
    'printer': {
        'type': 'string',
        'required': True,
        'empty': False
    },
    'remote_filename': {
        'type': 'string',
        'required': True,
        'empty': False
    },
    'label_variables': {
        'type': 'dict',
        'required': True,
        'empty': False
    }
})


@arcimoto.runtime.handler
@arcimoto.user.require('odoo.label.print')
def print_label_request(printer, remote_filename, label_variables):

    printer_server_uri = 'http://my.arcimoto.com:56425'
    if arcimoto.runtime.get_env() == 'dev':
        printer_server_uri = 'https://postman-echo.com/post'

    xml_data = '<nice_commands>'
    xml_data += f'<label name="c:/labels/{remote_filename}">'
    xml_data += f'<print_job printer="{printer}" quantity="1">'

    for key in label_variables:
        xml_data += f'<variable name="{key}">{label_variables[key]}</variable>'

    xml_data += '</print_job>'
    xml_data += '</label>'
    xml_data += '</nice_commands>'

    try:
        response = requests.post(printer_server_uri, xml_data)
        if response.status_code not in [200, 204]:
            raise ArcimotoException(f'Print Label Request Failed - status code: {response.status_code}, reason {response.reason}')

    except Exception as e:
        logger.warning(f'Print Label Request Failed with Exception: {e}')
        raise e

    return {}


lambda_handler = print_label_request
