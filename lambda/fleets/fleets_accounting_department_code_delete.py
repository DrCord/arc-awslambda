import arcimoto.args
import arcimoto.db
from arcimoto.exceptions import *
import arcimoto.runtime
import arcimoto.user

arcimoto.args.register({
    'id': {
        'type': 'integer',
        'required': True,
        'empty': False
    }
})


@arcimoto.runtime.handler
@arcimoto.user.require('fleets.group.write')
@arcimoto.db.transaction
def fleets_accounting_department_code_delete(id):

    try:
        cursor = arcimoto.db.get_cursor()
        # With materializes the "deleted" Query (in parens) as a result set
        # Allowing a standard count of deleted rows - Powerful...
        query = (
            'WITH deleted AS ( '
            'DELETE FROM '
            'accounting_department_code '
            'WHERE '
            'id = %s '
            'RETURNING *) '
            'SELECT count(*) FROM deleted'
        )

        cursor.execute(query, [id])
    except Exception as e:
        error_msg = f'Unable to delete accounting_department_code: ID - {id}  {e}'
        raise ArcimotoException(error_msg)

    return {"deleted_rows": cursor.fetchone()[0]}


lambda_handler = fleets_accounting_department_code_delete
