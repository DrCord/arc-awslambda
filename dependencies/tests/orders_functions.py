import logging

from arcimoto.exceptions import *
import arcimoto.runtime

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


def order_add_error_payment_notifier(args):
    return arcimoto.runtime.test_invoke_lambda('orders_order_add_error_payment_notifier', args, False)


def order_add_payment(args):
    return arcimoto.runtime.test_invoke_lambda('orders_order_add_payment', args, False)


def order_add_success_payment_notifier(args):
    return arcimoto.runtime.test_invoke_lambda('orders_order_add_success_payment_notifier', args, False)


def order_archive(args):
    return arcimoto.runtime.test_invoke_lambda('orders_order_archive', args, False)


def order_create(args):
    return arcimoto.runtime.test_invoke_lambda('orders_order_create', args, False)


def order_crm_update(args):
    return arcimoto.runtime.test_invoke_lambda('orders_order_crm_update', args, False)


def order_delete(args):
    return arcimoto.runtime.test_invoke_lambda('orders_order_delete', args, False)


def order_get(args):
    return arcimoto.runtime.test_invoke_lambda('orders_order_get', args, False)


def orders_get_highest_id():
    orders = orders_list().get('orders', [])
    return orders[-1].get('id', 0) if len(orders) else 0


def orders_list():
    return arcimoto.runtime.test_invoke_lambda('orders_orders_list', {}, False)


def order_queue_payment_error_cx(args):
    return arcimoto.runtime.test_invoke_lambda('orders_order_queue_payment_error_cx', args, False)


def order_queue_payment_success_customer(args):
    return arcimoto.runtime.test_invoke_lambda('orders_order_queue_payment_success_customer', args, False)


def order_queue_payment_success_cx(args):
    return arcimoto.runtime.test_invoke_lambda('orders_order_queue_payment_success_cx', args, False)


def order_ses_email(args):
    return arcimoto.runtime.test_invoke_lambda('orders_order_ses_email', args, False)


def order_get_test_dict():
    order = {
        "order_request": {
            "Order": {
                "items": [
                    {
                        "meta": [
                            {
                                "key": "trim",
                                "value": "fuv-sport-vinyl",
                                "keyLabel": "Trim",
                                "quantity": 1,
                                "unitPrice": 17900,
                                "description": "Sport Vinyl"
                            }
                        ],
                        "type": "reservation",
                        "model": "fuv",
                        "quantity": 1,
                        "modelName": "FUV",
                        "deliveryLeadTime": "120 Million Years, give or take a minor epoch"
                    }
                ],
                "referralCode": "Ref Code",
                "customerNotes": "These are my very custom specifications",
                "howDidYouHear": "I heard about you guys from CNN.",
                "deliveryMethod": "factory"
            },
            "Customer": {
                "dob": "01/03/1882",
                "email": "configurator+dev@arcimoto.com",
                "phone": "+19999999999",
                "lastName": "CustomerLast",
                "firstName": "CustomerFirst"
            },
            "ShippingAddress": {
                "city": "SACity",
                "state": "SAState",
                "country": "SACountry",
                "address1": "SAADDR1",
                "address2": "SAADDR2",
                "lastName": "SALast",
                "firstName": "SAFirst",
                "postalCode": "SAPost"
            },
            "BillingAddress": {
                "city": "BCity",
                "state": "BState",
                "country": "BCountry",
                "address1": "BADDR1",
                "address2": "BADDR2",
                "lastName": "BLast",
                "firstName": "BFirst",
                "postalCode": "BPost"
            },
            "orderRequestVersion": 1
        }
    }
    return order
