from arcimoto.exceptions import *
import arcimoto.runtime
import arcimoto.user
import arcimoto.db
import arcimoto.args


@arcimoto.runtime.handler
@arcimoto.user.require('fleets.group.read')
def fleets_accounting_department_codes_list():

    cursor = arcimoto.db.get_cursor()

    query = (
        'SELECT id, code, description '
        'FROM accounting_department_code'
    )
    cursor.execute(query)

    accounting_department_codes = []

    for record in cursor:
        accounting_department_codes.append(
            {
                'id': record['id'],
                'code': record['code'],
                'description': record['description']
            }
        )

    return {
        'accounting_department_codes': accounting_department_codes
    }


lambda_handler = fleets_accounting_department_codes_list
