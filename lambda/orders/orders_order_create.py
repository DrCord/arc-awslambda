import json
import random
import string
from datetime import datetime

import arcimoto.db
from arcimoto.exceptions import *
import arcimoto.runtime

arcimoto.args.register({
    'order_request': {
        'required': True,
        'type': 'dict',
        'schema': {
            'Order': {
                'required': True,
                'type': 'dict',
                'schema': {
                    'items': {
                        'required': True,
                        'type': 'list',
                        'schema': {
                            'type': 'dict',
                            'schema': {
                                'meta': {
                                    'required': True,
                                    'type': 'list',
                                    'schema': {
                                        'type': 'dict',
                                        'schema': {
                                            "key": {
                                                'required': True,
                                                'empty': False,
                                                'type': 'string'
                                            },
                                            "value": {
                                                'required': True,
                                                'empty': False,
                                                'type': 'string'
                                            },
                                            "keyLabel": {
                                                'required': True,
                                                'empty': False,
                                                'type': 'string'
                                            },
                                            "quantity": {
                                                'required': True,
                                                'empty': False,
                                                'type': 'number'
                                            },
                                            "unitPrice": {
                                                'required': True,
                                                'empty': False,
                                                'type': 'number'
                                            },
                                            "description": {
                                                'required': True,
                                                'empty': False,
                                                'type': 'string'
                                            },
                                        }
                                    }
                                },
                                "type": {
                                    'required': True,
                                    'empty': False,
                                    'type': 'string'
                                },
                                "model": {
                                    'required': True,
                                    'empty': False,
                                    'type': 'string'
                                },
                                "quantity": {
                                    'required': True,
                                    'empty': False,
                                    'type': 'number'
                                },
                                "modelName": {
                                    'required': True,
                                    'empty': False,
                                    'type': 'string'
                                },
                                "deliveryLeadTime": {
                                    'required': True,
                                    'type': 'string'
                                }
                            }
                        }
                    },
                    'referralCode': {'default': ''},
                    'customerNotes': {'default': ''},
                    'howDidYouHear': {'default': ''},
                    'deliveryMethod': {'default': 'factory'}
                }
            },
            'Customer': {
                'required': True,
                'type': 'dict',
                'schema': {
                    'dob': {'default': 'Unknown'},
                    'email': {
                        'required': True,
                        'type': 'string',
                        'regex': '^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
                    },
                    'phone': {
                        'required': True,
                        'empty': False,
                        'type': 'string'
                    },
                    'lastName': {
                        'required': True,
                        'empty': False,
                        'type': 'string'
                    },
                    'firstName': {
                        'required': True,
                        'empty': False,
                        'type': 'string'
                    },
                    'companyName': {'default': ''},
                    'driversLicenseState': {'default': ''},
                    'driversLicenseNumber': {'default': ''},
                    'insuranceCompanyName': {'default': ''},
                    'insurancePolicyNumber': {'default': ''}
                }
            },
            'BillingAddress': {
                'required': True,
                'type': 'dict',
                'schema': {
                    'city': {
                        'required': True,
                        'empty': False,
                        'type': 'string'
                    },
                    'state': {
                        'required': True,
                        'empty': False,
                        'type': 'string'
                    },
                    'country': {'default': "US"},
                    'lastName': {
                        'required': True,
                        'empty': False,
                        'type': 'string'
                    },
                    'firstName': {
                        'required': True,
                        'empty': False,
                        'type': 'string'
                    },
                    'address1': {
                        'required': True,
                        'type': 'string'
                    },
                    'address2': {'default': ''},
                    'postalCode': {
                        'required': True,
                        'empty': False
                    },
                }
            },
            'ShippingAddress': {
                'required': True,
                'type': 'dict',
                'schema': {
                    'city': {
                        'required': True,
                        'empty': False,
                        'type': 'string'
                    },
                    'state': {
                        'required': True,
                        'empty': False,
                        'type': 'string'
                    },
                    'country': {
                        'required': True,
                        'empty': False,
                        'type': 'string'
                    },
                    'lastName': {
                        'required': True,
                        'type': 'string'
                    },
                    'firstName': {
                        'required': True,
                        'type': 'string'
                    },
                    'address1': {
                        'required': True,
                        'empty': False,
                        'type': 'string'
                    },
                    'address2': {'default': ''},
                    'postalCode': {
                        'required': True,
                        'empty': False
                    },
                }
            }
        }
    }
})


@arcimoto.runtime.handler
@arcimoto.db.transaction
def orders_order_create(order_request):
    """Create the Order

    Keyword arguments:
        order_request -- type dict

    Returns:
         dict {"id": id|None}
    """

    order_json = None
    try:
        # raises error if dict or bad json
        order_json = json.loads(order_request)
    except Exception as e:
        # it was already a dict
        if type(order_request) is not dict:
            raise e
        else:
            order_json = order_request

    alphabet = string.ascii_lowercase + string.digits

    order_json['uuid'] = datetime.utcnow().strftime('%y%m%d') + ''.join(random.choices(alphabet, k=8))

    cursor = arcimoto.db.get_cursor()

    query = (
        'INSERT INTO order_request '
        '(order_request) VALUES (%s) '
        'RETURNING order_request->>\'uuid\' as id'
    )

    cursor.execute(query, [json.dumps(order_json)])

    result = {'id': None}
    if cursor.rowcount > 0:
        order_id = cursor.fetchone()['id']
        result = {'id': order_id}
    return result


lambda_handler = orders_order_create
