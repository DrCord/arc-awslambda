import logging

from arcimoto.exceptions import *
import arcimoto.db
import arcimoto.runtime
import arcimoto.user
import arcimoto.vehicle

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

arcimoto.args.register({
    'vin': {
        'type': 'string',
        'required': True
    },
    'group_id': {
        'type': 'integer',
        'required': True,
        'min': 1
    }
})


@arcimoto.runtime.handler
@arcimoto.user.require('fleets.group.write')
@arcimoto.db.transaction
def remove_vehicle_from_group(vin, group_id):
    vehicle_instance = arcimoto.vehicle.Vehicle(vin)
    vehicle_instance.remove_from_group(group_id)
    try:
        msg_part = f'Vehicle removed from fleet id {group_id}'
        arcimoto.note.VehicleNote(
            vin=vin,
            message=msg_part,
            tags=['fleets'],
            source=arcimoto.user.current().get_username()
        )
    except Exception as e:
        error_msg = f'Failure to create vehicle note for {vin} removal from vehicle group id {group_id}: - {e}'
        raise ArcimotoException(error_msg)
    vehicle_data = vehicle_instance.get()

    return vehicle_data


lambda_handler = remove_vehicle_from_group
