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
def orders_order_queue_payment_success_cx(records):
    """
    send an email containing an order with a successful pmt transaction

    Keyword arguments:
        records - type string (a valid JSON String) from SQS. Expected contents of
        message are
            [body][order]{order_request]
            [body][orderid]


    Returns:
        dict : {'statusCode', 'body'}
    """
    # message and body are AWS artifacts that are guaranted from SQS
    try:
        body = json.loads(records[0]['body'])
        order = json.loads(body['Message'])
    except Exception as e:
        raise ArcimotoArgumentError('Invalid Message')

    # order contents are validated prior to queueing. All other potential callers
    # of this lambda require input to be validated prior to usage.
    ses_args = {
        "order": order["order_request"],
        "order_id": order["id"],
        'target': 'CX_SUCCESS'
    }

    arcimoto.runtime.invoke_lambda("orders_order_ses_email", ses_args)

    return {
        'statusCode': 200,
        'body': "Successful lambda invocation for CX Success Dequeue"
    }


lambda_handler = orders_order_queue_payment_success_cx
