import arcimoto.runtime
import arcimoto.user
import arcimoto.db


@arcimoto.runtime.handler
@arcimoto.user.require('fleets.group.read')
@arcimoto.db.transaction
def fleets_vehicle_group_types_list():

    cursor = arcimoto.db.get_cursor()

    query = (
        'SELECT id, group_type '
        'FROM vehicle_group_type'
    )
    cursor.execute(query)

    group_types = []

    for record in cursor:
        group_types.append(
            {
                'id': record['id'],
                'group_type': record['group_type']
            }
        )

    return {
        'group_types': group_types
    }


lambda_handler = fleets_vehicle_group_types_list
