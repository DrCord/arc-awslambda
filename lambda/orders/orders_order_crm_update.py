import copy
import json
import logging
import requests

import arcimoto.args
from arcimoto.exceptions import *
import arcimoto.runtime

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

arcimoto.args.register({
    'order': {
        'type': 'dict',
        'required': True
    },
    'order_id': {
        'type': 'string',
        'required': True
    }
})

url_prefix = "https://api.hubapi.com/"
with open('hubspot_api_values.json') as f:
    magic_values = json.load(f)

vals = {}
payment_error = None
payment_held = None


@arcimoto.runtime.handler
def orders_order_crm_update(order, order_id):
    """Update Hubspot with certain data from the order

    Keyword arguments:
        order -- type dict
        order_id -- type string () order->>'uuid'

    Returns:
       Boolean: No exceptions detected - This is a 100% side effect function.
    """
    global vals
    global payment_error
    global payment_held

    vals = magic_values[arcimoto.runtime.get_env()]

    token = get_token()

    headers = {
        'content-type': 'application/json',
        'authorization': 'Bearer %s' % token
    }

    deal_id = None

    payment_error = (order["payment"]["status"] == "error")
    payment_held = (order["payment"]["status"] == "held")

    contact_id = crm_create_or_update_contact(order, headers)

    if not payment_error:
        deal_id = crm_insert_deal(contact_id, order, order_id, headers)
        add_line_item(deal_id, order, headers)

    crm_insert_note(deal_id, contact_id, order, order_id, headers)

    return True


def crm_create_or_update_contact(order, headers):
    order_email = order.get("Customer", {}).get("email", None)
    url = f'{url_prefix}contacts/v1/contact/createOrUpdate/email/{order_email}'

    if order_email is None:
        raise ArcimotoException('Unable to get email from order')

    # Note that the order structure is tested at original insert for correctness.
    data = json.dumps({
        "properties": [
            {
                "property": "email",
                "value": order['Customer']['email']
            },
            {
                "property": "firstname",
                "value": order['Customer']['firstName']
            },
            {
                "property": "lastname",
                "value": order['Customer']['lastName']
            },
            {
                "property": "lifecyclestage",
                "value": "customer"
            },
            {
                "property": "address",
                "value": order['ShippingAddress']['address1']
            },
            {
                "property": "address_2",
                "value": order['ShippingAddress']['address2']
            },
            {
                "property": "city",
                "value": order['ShippingAddress']['city']
            },
            {
                "property": "state",
                "value": order['ShippingAddress']['state']
            },
            {
                "property": "zip",
                "value": order['ShippingAddress']['postalCode']
            },
            {
                "property": "country",
                "value": order['ShippingAddress']['country']
            },
            {
                "property": "phone",
                "value": order['Customer']['phone']
            },
            {
                "property": "hs_pipeline",
                "value": vals['customer_pipeline']
            },
            {
                "property": "last_products_bought_product_1_name",
                "value": "Reservation"
            }
        ]
    })

    r = requests.post(data=data, url=url, headers=headers)

    contact_data = json.loads(r.text)
    return contact_data["vid"]


def crm_insert_deal(contact_id, order, order_id, headers):
    url = f'{url_prefix}deals/v1/deal'

    order_copy = copy.deepcopy(order)
    det = order_copy['Order']['items'].pop(0)

    dealname = f"#{order_id} { order['Customer']['firstName']} { order['Customer']['lastName']}"
    deliverynotes = order["Order"]["deliveryMethod"]
    vehicletype = det["modelName"]

    estimatedPrice = 0
    for d in det['meta']:
        # sum estimated total price
        for k, v in d.items():
            if k == "unitPrice" and isfloat(v):
                estimatedPrice += v

    data = json.dumps({
        "associations": {
            "associatedVids": [
                contact_id
            ]
        },
        "properties": [
            {
                "name": "dealname",
                "value": dealname
            },
            {
                "name": "pipeline",
                "value": vals['pipeline']
            },
            {
                "name": "dealstage",
                "value": get_stage(order_copy['payment']['status'])
            },
            {
                "name": "amount",
                "value": estimatedPrice
            },
            {
                "name": "dealtype",
                "value": vals['dealtype']
            },
            {
                "name": "delivery_notes",
                "value": deliverynotes
            },
            {
                "name": "vehicle_type",
                "value": vehicletype
            },
            {
                "name": "address",
                "value": f"{order['ShippingAddress']['address1']}\r\n{order['ShippingAddress']['address2']}"
            },
            {
                "name": "city",
                "value": order['ShippingAddress']['city']
            },
            {
                "name": "state",
                "value": order['ShippingAddress']['state']
            },
            {
                "name": "postal_code",
                "value": order['ShippingAddress']['postalCode']
            }
        ]
    })

    r = requests.post(url, headers=headers, data=data)
    data = json.loads(r.text)
    return data["dealId"]


def add_line_item(deal_id, order, headers):
    global logger
    urlitem = f'{url_prefix}crm-objects/v1/objects/line_items'
    urlassoc = f'{url_prefix}crm-associations/v1/associations'

    payment = order['payment']['amount']
    payloaddata = json.dumps([
        {
            "name": "hs_product_id",
            "value": vals['reservationid']
        },
        {
            "name": "quantity",
            "value": "1"
        },
        {
            "name": "price",
            "value": payment
        }
    ])
    try:
        r = requests.post(urlitem, headers=headers, data=payloaddata)
        data = json.loads(r.text)
        itemId = data.get("objectId", None)

        if itemId is not None:
            payloaddata = json.dumps({
                "fromObjectId": itemId,
                "toObjectId": deal_id,
                "category": "HUBSPOT_DEFINED",
                "definitionId": vals['lineitemtodeallink']
            })

            r = requests.put(urlassoc, headers=headers, data=payloaddata)
        else:
            raise ArcimotoException("Unable to add Line Item")
    except Exception as e:
        env = arcimoto.runtime.get_env()
        error_msg = f'  ENV:{env} {e} - payload: {payloaddata}, response-text: {data}, Config: {vals}'
        logger.info(error_msg)


def crm_insert_note(deal_id, contact_id, order, order_id, headers):
    url = f'{url_prefix}engagements/v1/engagements'
    order_copy = copy.deepcopy(order)
    note = []

    # pass a copy of the order to formatting methods explicitly for popping
    note.append(note_header(order_copy, order_id))
    note.append(note_extra_info(order_copy))
    note.append(note_fuv_configuration(order_copy))

    note = ''.join(note)

    payload = {
        "engagement": {
            "active": 'true',
            "type": "NOTE"
        },
        "associations": {
            "contactIds": [contact_id]
        },
        "metadata": {
            "body": note
        }
    }

    # if there is a deal add the note to the deal as well
    if deal_id is not None:
        payload['associations']["dealIds"] = [deal_id]

    payload_json = json.dumps(payload)

    requests.request("POST", url, data=payload_json, headers=headers)


def note_header(order, order_id):
    header = ''
    order_copy = copy.deepcopy(order)
    det = order_copy['Order']['items'].pop(0)
    pmt = order_copy["payment"]

    if payment_error:
        header = f'Payment Failed for Order #{order_id} {pmt["provider"]} Transaction ID: {pmt["transactionId"]}'
    elif payment_held:
        header = f'Payment Held for Order #{order_id} {pmt["provider"]} Transaction ID: {pmt["transactionId"]}'
    else:
        header = f'New Customer Order #{order_id} {det["modelName"]} {det["type"]}'

    return header


def note_fuv_configuration(order):
    order_copy = copy.deepcopy(order)
    det = order_copy['Order']['items'].pop(0)

    fuv_conf = []
    fuv_conf.append('<p>')
    fuv_conf.append('<figure>')
    fuv_conf.append("<figcaption>FUV Configuration</figcaption>")
    fuv_conf.append("<ul>")
    for m in det['meta']:
        fuv_conf.append(f'<li>{m["keyLabel"]} -- {m["description"]} -- {format_price(m["unitPrice"])} </li>')
    fuv_conf.append("</ul>")
    fuv_conf.append('</figure>')
    fuv_conf.append("</p>")

    return ' '.join(fuv_conf)


def note_extra_info(order):
    order_copy = copy.deepcopy(order)
    det = order_copy['Order']['items'].pop(0)

    info = [
        '<p>'
        'Order Information',
        f'Paid: {order_copy["payment"]["amount"]}',
        f'Delivery Method: {order_copy["Order"]["deliveryMethod"]}',
        f'Delivery Lead Time: {det["deliveryLeadTime"]}',
        f'How I heard:  {order_copy["Order"]["howDidYouHear"]}',
        f'Referral Code:  {order_copy["Order"]["referralCode"]}',
        f'Notes: {order_copy["Order"]["customerNotes"]}',
        '</p>'
    ]

    return '<br/>'.join(info)


def format_price(v):
    formatted = v
    if v == 0:
        formatted = "No Charge"
    else:
        formatted = "${:,.2f}".format(float(v))
    return formatted


def get_token():
    env = arcimoto.runtime.get_env()
    key = arcimoto.runtime.get_secret(f'orders.hubspot.token.{env}').get('token', None)
    return key


def isfloat(num):
    try:
        float(num)
        return True
    except ValueError:
        return False


def get_stage(status):
    crmval = vals['dealstage_ordered']
    if status in ['error', 'held']:
        crmval = vals['dealstage_pendingfailed']
    return crmval


lambda_handler = orders_order_crm_update
