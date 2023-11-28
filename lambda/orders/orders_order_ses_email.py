import boto3
import copy
import json
from datetime import date

import logging

from arcimoto.exceptions import *
import arcimoto.runtime
import arcimoto.args

arcimoto.args.register({
    'order': {
        'type': 'dict',
        'required': True
    },
    'order_id': {
        'type': 'string',
        'required': True
    },
    'target': {
        'type': 'string',
        'required': True
    }


})

AWS_REGION = 'us-west-2'

# This address must be verified with Amazon SES.
SENDER = 'Arcimoto <no-reply@arcimoto.com>'


@arcimoto.runtime.handler
def orders_order_ses_email(order, order_id, target):
    global AWS_REGION, SENDER

    env = arcimoto.runtime.get_env()

    orderx = copy.deepcopy(order)

    cx_success_email = arcimoto.runtime.get_secret(f'orders.email.cx.success.{env}').get('email', None)
    cx_error_email = arcimoto.runtime.get_secret(f'orders.email.cx.error.{env}').get('email', None)
    customer_email = orderx['Customer']['email']

    if target == 'CUSTOMER_SUCCESS':
        recipients = [customer_email]
        order_template = f'TEL_orders_order_success_customer_{env}'
    elif target == 'CX_ERROR':
        recipients = [cx_error_email]
        order_template = f'TEL_orders_order_success_CX_{env}'
    else:
        recipients = [cx_success_email]
        order_template = f'TEL_orders_order_success_CX_{env}'

    orderx['subject'] = subject(order, order_id)

    # Order Munging for happy SES Emails
    # Formatting the data for display
    orderx['estimatedPrice'] = 0
    for d in orderx['Order']['items'][0]['meta']:
        # sum estimated total price
        for k, v in d.items():
            if k == "unitPrice" and isfloat(v):
                orderx['estimatedPrice'] += v
        # currency formatter
        d.update((k, formatPrice(v)) for k, v in d.items() if k == 'unitPrice')

    orderx['estimatedPrice'] = formatPrice(orderx['estimatedPrice'])
    orderx['payment']['amount'] = formatPrice(orderx['payment']['amount'])

    orderx['payment']['alert'] = ''

    # [payment][paymentMethod] is required in add_payment and is guaranteed here
    if orderx['payment']['paymentMethod'] == 'creditCard':
        orderx['payment']['paymentMethod'] = 'Credit Card'
        orderx['payment']['alert'] = 'Your card will be billed the Total Due Now'
    elif orderx['payment']['paymentMethod'] == 'ach':
        orderx['payment']['paymentMethod'] = 'Direct Bank Transfer'

    # allows template test for held payments
    if orderx['payment']['status'] == 'held':
        orderx['payment']['held'] = '1'
    elif orderx['payment']['status'] == 'error':
        orderx['payment']['error'] = '1'

    orderx['currentYear'] = date.today().year

    # Change data shape to remove lists that are difficult for Mustache to walk in SES template
    details = orderx['Order']['items'].pop(0)
    orderx['Order'].pop('items', None)
    orderx['Order'] = {**orderx["Order"], **details}
    orderx['order_id'] = order_id

    ses_client = boto3.client('ses', region_name=AWS_REGION)

    response = ses_client.send_templated_email(
        Destination={
            'ToAddresses': recipients
        },
        Source=SENDER,
        ReplyToAddresses=[SENDER],
        Template=order_template,
        TemplateData=json.dumps(orderx),
        SourceArn=arcimoto.runtime.arn_sections_join('ses', 'identity/no-reply@arcimoto.com'),
        ReturnPathArn=arcimoto.runtime.arn_sections_join('ses', 'identity/no-reply@arcimoto.com')
    )

    return response


def subject(order, order_id):
    order_c = copy.deepcopy(order)
    status = order_c['payment']['status']
    details = order_c['Order']['items'].pop(0)
    model = details['modelName']
    name = order_c['Customer']['firstName']
    if status == 'error':
        subject = f'Failed Order #{order_id}'
    elif status == 'held':
        subject = f'New Order #{order_id} (Pending Payment)'
    else:
        subject = f'New Arcimoto {model} for {name}'

    return subject


def isfloat(num):
    try:
        float(num)
        return True
    except ValueError:
        return False


def formatPrice(v):
    formatted = v
    if v == 0:
        formatted = "No Charge"
    else:
        formatted = "${:,.2f}".format(float(v))
    return formatted


lambda_handler = orders_order_ses_email
