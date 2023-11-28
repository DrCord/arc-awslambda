import logging
from arcimoto.exceptions import *
import arcimoto.runtime
import arcimoto.args
import arcimoto.user
import arcimoto.vehicle

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

arcimoto.args.register({
    'vin': {
        'type': 'string',
        'required': True
    },
    'verification_id': {
        'type': 'string',
        'default': ''
    },
    'pin': {
        'type': 'string',
        'default': None,
        'nullable': True,
        'minlength': 6,
        'maxlength': 6,
        'regex': '^[0-9]+$'
    }
})


@arcimoto.runtime.handler
def managed_session_start(vin, verification_id, pin):
    vehicle = arcimoto.vehicle.Vehicle(vin)
    if not vehicle.exists:
        raise ArcimotoNotFoundError(f'Invalid vin: {vin}')
    current_user = arcimoto.user.current()
    if not vehicle.validate_user_access(current_user.username):
        current_user.assert_permission('managed_session.session.start')

    try:
        managed_session = vehicle.managed_session_start(
            arcimoto.user.current().username,
            verification_id,
            pin
        )
    except Exception as e:
        raise ArcimotoException(e)

    return managed_session


lambda_handler = managed_session_start
