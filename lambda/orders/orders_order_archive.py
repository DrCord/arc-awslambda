import arcimoto.db
from arcimoto.exceptions import *
import arcimoto.runtime
import arcimoto.user

arcimoto.args.register({
    'order_id': {
        'type': 'string',
        'required': True
    }
})


@arcimoto.runtime.handler
@arcimoto.db.transaction
def orders_order_archive(order_id):
    """Archive the Order set the the archived_at Date

    Keyword arguments:
        order_id -- type string () order_request->>'uuid'

    Returns:
        dict: {"id": id, "archived_at": UTCSTR}|{}
    """

    query = (
        'UPDATE order_request '
        'SET archived_at  = now() '
        'WHERE order_request->>\'uuid\' = %s '
        'AND archived_at is NULL '
        'RETURNING order_request->>\'uuid\' as id, archived_at'
    )

    cursor = arcimoto.db.get_cursor()
    cursor.execute(query, [order_id])

    result = {}
    if cursor.rowcount > 0:
        row = cursor.fetchone()

        result = {
            'id': row['id'],
            'archived_at': arcimoto.db.datetime_record_output(row['archived_at'])
        }
    return result


lambda_handler = orders_order_archive
