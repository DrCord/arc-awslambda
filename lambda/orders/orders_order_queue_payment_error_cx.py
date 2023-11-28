import json

from arcimoto.exceptions import *
import arcimoto.runtime
import arcimoto.args

arcimoto.args.register({
    'Records': {
        'rename': 'records'
    },
    'records': {
        'type': 'list',
        'required': True,
        'empty': False
    }
})


@arcimoto.runtime.handler
def orders_order_queue_payment_error_cx(records):
    """
    send an email containing an order with a unsuccessful pmt transaction
    The initial json is an AWS queueing artifact

    Keyword arguments:
        records - type string (a valid JSON String)

    Returns:
        dict : {'statusCode', 'body'}
    """

    # message and body are AWS artifacts that are guaranted from SQS
    try:
        body = json.loads(records[0]['body'])
        order = json.loads(body['Message'])
    except Exception as e:
        raise ArcimotoArgumentError(f'Unable to process message {e}')

    ses_args = {
        "order": order["order_request"],
        "order_id": order["id"],
        'target': 'CX_ERROR'
    }

    arcimoto.runtime.invoke_lambda("orders_order_ses_email", ses_args)

    return {
        'statusCode': 200,
        'body': "Successful lambda invocation for CX Error Dequeue"
    }


lambda_handler = orders_order_queue_payment_error_cx
