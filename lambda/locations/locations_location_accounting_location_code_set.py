from arcimoto.exceptions import *
import arcimoto.runtime
import arcimoto.user
import arcimoto.db

arcimoto.args.register({
    'location_id': {
        'type': 'integer',
        'required': True,
        'min': 1
    },
    'accounting_location_code_id': {
        'type': 'integer',
        'required': True,
        'min': 1,
        'nullable': True
    }
})


@arcimoto.runtime.handler
@arcimoto.user.require('locations.update')
@arcimoto.db.transaction
def locations_location_accounting_location_code_set(location_id, accounting_location_code_id):

    cursor = arcimoto.db.get_cursor()

    if not location_exists(location_id):
        raise ArcimotoNotFoundError('Invalid location id')

    if accounting_location_code_id is None:
        query = (
            'DELETE FROM location_join_accounting_location_code '
            'WHERE location_id = %s'
        )
        cursor.execute(query, [location_id])
    else:
        query = (
            'INSERT INTO location_join_accounting_location_code '
            '(location_id, accounting_location_code_id) VALUES (%s, %s) '
            'ON CONFLICT ON CONSTRAINT ljalc_location_id_unique DO UPDATE '
            'SET accounting_location_code_id=excluded.accounting_location_code_id'
        )
        cursor.execute(query, [location_id, accounting_location_code_id])

    return {}


def location_exists(id):
    return arcimoto.db.check_record_exists('locations', {'id': id})


lambda_handler = locations_location_accounting_location_code_set
