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
    },
    'description': {
        'type': 'string',
        'default': '',
        'maxlength': 64
    }
})


@arcimoto.runtime.handler
@arcimoto.user.require('fleets.group.write')
@arcimoto.db.transaction
def fleets_accounting_department_code_create(code, description):

    cursor = arcimoto.db.get_cursor()

    try:
        query = (
            'INSERT INTO '
            'accounting_department_code (code, description) VALUES (%s, %s)'
            'ON CONFLICT DO NOTHING '
            'RETURNING id'
        )
        cursor.execute(query, [code, description])
        result_set = cursor.fetchone()
        department_code_id = result_set['id'] if result_set is not None else None

    except Exception as e:
        raise ArcimotoException(f'Unable to insert Accounting Department Code Record with code {code}: {e}') from e

    return {'id': department_code_id}


lambda_handler = fleets_accounting_department_code_create
