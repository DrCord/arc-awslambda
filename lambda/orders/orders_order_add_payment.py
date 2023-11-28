import json

import arcimoto.db
from arcimoto.exceptions import *
import arcimoto.runtime
import arcimoto.user

arcimoto.args.register({
    'order_id': {
        'type': 'string',
        'required': True
    },
    'payment': {
        'required': True,
        'type': 'dict',
        'schema': {
            'amount': {
                'required': True,
                'empty': False,
                'type': 'number'
            },
            'status': {
                'required': True,
                'type': 'string',
                'allowed': ['success', 'error', 'approved', 'held']
            },
            'provider': {
                'type': 'string'
            },
            'paymentMethod': {
                'required': True,
                'empty': False,
                'type': 'string'
            },
            'transactionId': {
                'type': 'string',
                'required': False,
                'default': ' '
            },
            'error': {
                'type': 'string',
                'required': False
            }
        }
    }
})


@arcimoto.runtime.handler
@arcimoto.db.transaction
def orders_order_add_payment(order_id, payment):
    """Add Payment to the Order by adding or overwriting the order_request.payment

    Keyword arguments:
        order_id - type string
        payment - type dict | valid JSON string

    Returns:
        row : type dict (row in DB | {})
    """

    if not isinstance(payment, dict):
        try:
            payment = json.loads(payment)
        except Exception as e:
            raise ArcimotoException(f'Unable to make successful payment {e}')

    payment_status = payment.get('status', None)

    cursor = arcimoto.db.get_cursor()
    query = (
        'UPDATE order_request '
        'SET order_request = order_request || %s::jsonb '
        'WHERE order_request->>\'uuid\' = %s '
        'RETURNING order_request->>\'uuid\' as id, created_at, archived_at, order_request'
    )

    payment_str = json.dumps({'payment': payment})
    cursor.execute(query, [payment_str, order_id])
    result = {}
    if cursor.rowcount > 0:
        row = cursor.fetchone()
        result['id'] = row['id']
        result['created_at'] = arcimoto.db.datetime_record_output(row['created_at'])
        result['archived_at'] = arcimoto.db.datetime_record_output(row['archived_at'])
        result['order_request'] = row['order_request']

        if payment_status in ['success', 'held', 'approved']:
            arcimoto.runtime.invoke_lambda("orders_order_add_success_payment_notifier", {"order_id": order_id, "order": result})
        else:
            arcimoto.runtime.invoke_lambda("orders_order_add_error_payment_notifier", {"order_id": order_id, "order": result})

    return result


lambda_handler = orders_order_add_payment
