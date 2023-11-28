import logging

from arcimoto.exceptions import *
import arcimoto.runtime
import arcimoto.user
import arcimoto.db

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

arcimoto.args.register({
    'username': {
        'type': 'string',
        'required': True,
        'empty': False
    }
})


@arcimoto.runtime.handler
def user_groups_get(username):
    global logger

    # users are allowed to get their own groups - otherwise need proper permission
    if username != arcimoto.user.current().username:
        arcimoto.user.current().assert_permission('fleets.group.read')

    cursor = arcimoto.db.get_cursor()

    user_groups = []

    query = ('SELECT '
             'ujvg.vehicle_group,'
             'vg.name, '
             '(SELECT array_agg(vjvg.vin) from vehicle_join_vehicle_group vjvg WHERE vjvg.group_id = ujvg.vehicle_group) AS vins '
             'from users_join_vehicle_group ujvg '
             'LEFT JOIN vehicle_group vg ON ujvg.vehicle_group = vg.id '
             'WHERE username=%s '
             'ORDER BY ujvg.vehicle_group ASC')
    cursor.execute(query, [username])

    for record in cursor:
        user_groups.append(
            {
                'id': record['vehicle_group'],
                'name': record['name'],
                'vins': record['vins']
            }
        )

    return {'user_groups': user_groups}


lambda_handler = user_groups_get
