from arcimoto.exceptions import *
import arcimoto.db
import arcimoto.runtime
import arcimoto.user


@arcimoto.runtime.handler
def orders_orders_list():
    """Get a list of unarchived orders

    Returns:
        type dict -  {"orders": listOfOrders}
    """

    cursor = arcimoto.db.get_cursor()

    query = (
        'SELECT order_request->>\'uuid\' as id, id as auto_id, order_request, created_at '
        'FROM order_request '
        'WHERE archived_at IS NULL '
        'ORDER BY created_at DESC LIMIT 100'
    )

    cursor.execute(query)

    result = []
    for record in cursor:
        result.append(
            {
                'id': record['id'],
                'auto_id': record['auto_id'],
                'order_request': record['order_request'],
                'created_at': arcimoto.db.datetime_record_output(record['created_at'])
            }
        )

    return {
        'orders': result
    }


lambda_handler = orders_orders_list
