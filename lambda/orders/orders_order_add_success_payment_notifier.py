import json
import boto3
import logging

from arcimoto.exceptions import *
import arcimoto.runtime

arcimoto.args.register({
    'order_id': {
        'type': 'string',
        'required': True
    },
    'order': {
        'required': True,
        'type': 'dict'
    }
})


@arcimoto.runtime.handler
def orders_order_add_success_payment_notifier(order_id, order):
    """Sends the order in payload to SNS

    Keyword arguments:
        order_id - type string
        order - type dict | valid JSON string

    Returns:
        success - boolean
    """
    env = arcimoto.runtime.get_env()
    arn = arcimoto.runtime.arn_sections_join('sns', f'orders_payment_success_{env}')
    sns = boto3.client('sns')

    attributes = {
        "order_id": {
            "DataType": "String",
            "StringValue": f"{order_id}"
        }
    }

    response = sns.publish(
        TopicArn=arn,
        Message=json.dumps(order),
        MessageAttributes=attributes
    )

    return response


lambda_handler = orders_order_add_success_payment_notifier
