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
def managed_session_get(id=None, vin=None):
    current_user = arcimoto.user.current()
    if vin is not None:
        vehicle = arcimoto.vehicle.Vehicle(vin)
        if not vehicle.exists:
            raise ArcimotoNotFoundError(f'Invalid vin: {vin}')
        if not vehicle.validate_user_access(current_user.username):
            current_user.assert_permission('managed_session.session.read')
    else:
        current_user.assert_permission('managed_session.session.read')

    cursor = arcimoto.db.get_cursor()
    query = (
        'SELECT id, vin, pin, initialization, completion, creator, verification_id '
        'FROM managed_sessions '
    )
    if vin is not None:
        query += 'WHERE vin = %s'
        params = [vin]
    else:
        query += 'WHERE id = %s'
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
                    'creator': item['creator'],
                    'verification_id': item['verification_id']
                }
                managed_sessions.append(managed_session)
    except Exception as e:
        raise ArcimotoException(e)

    return {
        'managed_sessions': managed_sessions
    }


lambda_handler = managed_session_get
