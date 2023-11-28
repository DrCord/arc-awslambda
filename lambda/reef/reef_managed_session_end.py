import logging
from arcimoto.exceptions import *
import arcimoto.runtime
import arcimoto.args
import arcimoto.user
import arcimoto.db
import arcimoto.vehicle

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

arcimoto.args.register({
    'vin': {
        'type': 'string',
        'required': True
    }
})


@arcimoto.runtime.handler
def reef_managed_session_end(vin):
    vehicle = arcimoto.vehicle.Vehicle(vin)
    if not vehicle.validate_access_reef():
        raise ArcimotoPermissionError(f'Unauthorized: {vin} not controlled by REEF')
    if not vehicle.exists:
        raise ArcimotoNotFoundError(f'Invalid vin: {vin}')

    try:
        managed_session = vehicle.reef_managed_session_end()
    except Exception as e:
        raise ArcimotoREEFAlertException(e)

    return managed_session


lambda_handler = reef_managed_session_end
