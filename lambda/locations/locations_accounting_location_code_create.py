import arcimoto.args
import arcimoto.db
from arcimoto.exceptions import *
import arcimoto.runtime
import arcimoto.user


arcimoto.args.register({
    'code': {
        'type': 'string',
        'required': True,
        'empty': False,
        'maxlength': 10
    }
})


@arcimoto.runtime.handler
@arcimoto.user.require('locations.code.create')
@arcimoto.db.transaction
def locations_accounting_location_code_create(code):

    cursor = arcimoto.db.get_cursor()

    try:
        query = (
            'INSERT INTO '
            'accounting_location_code (code) VALUES (%s)'
            'ON CONFLICT DO NOTHING '
            'RETURNING id'
        )
        cursor.execute(query, [code])
        result_set = cursor.fetchone()
        accounting_location_code = result_set['id'] if result_set is not None else None

    except Exception as e:
        raise ArcimotoException(f'Unable to insert Accounting Location Code Record with code {code}: {e}') from e

    return {'id': accounting_location_code}


lambda_handler = locations_accounting_location_code_create
