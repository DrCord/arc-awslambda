from arcimoto.exceptions import *
import arcimoto.runtime
import arcimoto.user
import arcimoto.db

arcimoto.args.register({
    'vehicle_group_id': {
        'type': 'integer',
        'required': True,
        'min': 1
    },
    'accounting_department_code_id': {
        'type': 'integer',
        'required': True,
        'min': 1,
        'nullable': True
    }
})


@arcimoto.runtime.handler
@arcimoto.user.require('fleets.group.write')
@arcimoto.db.transaction
def fleets_vehicle_group_accounting_department_code_set(vehicle_group_id, accounting_department_code_id):

    cursor = arcimoto.db.get_cursor()

    if not vehicle_group_exists(vehicle_group_id):
        raise ArcimotoNotFoundError('Invalid vehicle_group id')

    if accounting_department_code_id is None:
        query = (
            'DELETE FROM vehicle_group_join_accounting_department_code '
            'WHERE vehicle_group_id = %s'
        )
        cursor.execute(query, [vehicle_group_id])
    else:
        query = (
            'INSERT INTO vehicle_group_join_accounting_department_code '
            '(vehicle_group_id, accounting_department_code_id) VALUES (%s, %s) '
            'ON CONFLICT ON CONSTRAINT vgjadc_vehicle_group_id_unique DO UPDATE '
            'SET accounting_department_code_id=excluded.accounting_department_code_id'
        )
        cursor.execute(query, [vehicle_group_id, accounting_department_code_id])

    return {}


def vehicle_group_exists(id):
    return arcimoto.db.check_record_exists('vehicle_group', {'id': id})


lambda_handler = fleets_vehicle_group_accounting_department_code_set
