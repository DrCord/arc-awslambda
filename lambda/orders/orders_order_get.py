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
def orders_order_get(order_id):
    """Get the Order for an id

    Keyword arguments:
        order_id -- {order_request->>'uuid': Value}
    Returns:
        type dict - {DB Row}|{}
    """

    cursor = arcimoto.db.get_cursor()

    query = (
        'SELECT order_request->>\'uuid\' as id, order_request, created_at, archived_at '
        'FROM order_request '
        'WHERE order_request->>\'uuid\' = %s'
    )

    cursor.execute(query, [order_id])
    if cursor.rowcount != 1:
        raise ArcimotoArgumentError('Invalid id')
    result = {}
    if cursor.rowcount > 0:
        result = cursor.fetchone()
        result['created_at'] = arcimoto.db.datetime_record_output(result['created_at'])
        result['archived_at'] = arcimoto.db.datetime_record_output(result['archived_at'])

    return result


lambda_handler = orders_order_get
