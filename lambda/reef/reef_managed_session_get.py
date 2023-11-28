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
    'id': {
        'type': 'integer',
        'min': 1,
        'excludes': 'vin',
        'required': True
    },
    'vin': {
        'type': 'string',
        'excludes': 'id',
        'required': True
    }
})


@arcimoto.runtime.handler
def reef_managed_session_get(id=None, vin=None):
    if vin is not None:
        vehicle = arcimoto.vehicle.Vehicle(vin)
        if not vehicle.validate_access_reef():
            raise ArcimotoPermissionError(f'Unauthorized: {vin} not controlled by REEF')
        if not vehicle.exists:
            raise ArcimotoNotFoundError(f'Invalid vin: {vin}')

    cursor = arcimoto.db.get_cursor()
    query = (
        'SELECT id, vin, pin, initialization, completion, verification_id '
        'FROM managed_sessions_reef '
        'WHERE '
    )
    if vin is not None:
        query += 'vin = %s'
        params = [vin]
    else:
        query += 'id = %s'
        params = [id]
    managed_sessions = []
    try:
        cursor.execute(query, params)
        result = cursor.fetchall()
        if result is not None:
            for item in result:
                managed_session = {
                    'id': item['id'],
                    'vin': item['vin'],
                    'pin': item['pin'],
                    'initialization': arcimoto.db.datetime_record_output(item['initialization']),
                    'completion': arcimoto.db.datetime_record_output(item['completion']) if item['completion'] is not None else 'active',
                    'verification_id': item['verification_id']
                }
                managed_sessions.append(managed_session)
    except Exception as e:
        raise ArcimotoREEFAlertException(e)

    return {
        'managed_sessions': managed_sessions
    }


lambda_handler = reef_managed_session_get
