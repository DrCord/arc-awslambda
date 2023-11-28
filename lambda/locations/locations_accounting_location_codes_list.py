from arcimoto.exceptions import *
import arcimoto.runtime
import arcimoto.user
import arcimoto.db
import arcimoto.args


@arcimoto.runtime.handler
def locations_accounting_location_codes_list():

    cursor = arcimoto.db.get_cursor()

    query = (
        'SELECT id, code '
        'FROM accounting_location_code'
    )
    cursor.execute(query)

    accounting_location_codes = []

    for record in cursor:
        accounting_location_codes.append(
            {
                'id': record['id'],
                'code': record['code']
            }
        )

    return {
        'accounting_location_codes': accounting_location_codes
    }


lambda_handler = locations_accounting_location_codes_list
