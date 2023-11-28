import arcimoto.db
from arcimoto.exceptions import *
import arcimoto.runtime

arcimoto.args.register({
    'order_id': {
        'type': 'string',
        'required': True
    }
})


@arcimoto.runtime.handler
@arcimoto.db.transaction
def orders_order_delete(order_id):
    """Delete the Order for an id

    Keyword arguments:
        order_id -- {order_id: Value}

    Returns:
        type dict - {"deleted_rows": rowCount}

    Throws:
        ArcimotoException on a DB Error
    """

    cursor = arcimoto.db.get_cursor()

    try:
        cursor = arcimoto.db.get_cursor()
        query = (
            'WITH deleted AS ( '
            'DELETE FROM '
            'order_request '
            'WHERE '
            'order_request->>\'uuid\' = %s '
            'RETURNING *) '
            'SELECT count(*) FROM deleted'
        )

        cursor.execute(query, [order_id])
    except Exception as e:
        error_msg = f'Unable to delete Order Request: ID - {order_id}  {e}'
        raise ArcimotoException(error_msg)

    return {"deleted_rows": cursor.fetchone()[0]}


lambda_handler = orders_order_delete
