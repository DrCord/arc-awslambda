import logging
from arcimoto.exceptions import *
import arcimoto.runtime
import arcimoto.user
import arcimoto.db

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


@arcimoto.runtime.handler
@arcimoto.user.require('managed_session.session.read')
def managed_session_list():

    cursor = arcimoto.db.get_cursor()
    query = (
        'SELECT id, vin, pin, initialization, completion, creator, verification_id '
        'FROM managed_sessions '
        'ORDER BY id ASC'
    )
    managed_sessions = []
    try:
        cursor.execute(query)
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


lambda_handler = managed_session_list
