import logging
from arcimoto.exceptions import *
import arcimoto.runtime
import arcimoto.user
import arcimoto.db

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


@arcimoto.runtime.handler
@arcimoto.db.transaction
def reef_managed_session_list():

    cursor = arcimoto.db.get_cursor()
    # limits to VINs in REEF Vehicle Group
    query = (
        'SELECT id, vin, pin, initialization, completion, verification_id '
        'FROM managed_sessions_reef '
        'WHERE vin IN ('
        'SELECT DISTINCT(vjvg.vin) '
        'FROM vehicle_join_vehicle_group AS vjvg '
        'LEFT JOIN vehicle_group vg '
        'ON vg.id=vjvg.group_id '
        "WHERE vg.name = 'REEF'"
        ') '
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
                    'verification_id': item['verification_id']
                }
                managed_sessions.append(managed_session)
    except Exception as e:
        raise ArcimotoREEFAlertException(e)

    return {
        'managed_sessions': managed_sessions
    }


lambda_handler = reef_managed_session_list
