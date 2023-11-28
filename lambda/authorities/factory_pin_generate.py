import logging
import random

from arcimoto.exceptions import *
import arcimoto.runtime
import arcimoto.args
import arcimoto.user
import arcimoto.db

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

arcimoto.args.register({
    'vin': {
        'type': 'string',
        'required': True
    },
    'preserve_pin': {
        'type': 'boolean',
        'default': False,
        'nullable': True,
        'coerce': (str, arcimoto.args.arg_boolean_empty_string_to_null)
    }
})


@arcimoto.runtime.handler
@arcimoto.user.require('vehicles.vehicle.provision')
@arcimoto.db.transaction
def factory_pin_generate(vin, preserve_pin=False):
    global logger

    pin = None
    result = {}

    # reject certain 'bad pins'
    disallowedPins = [
        '000000',
        '111111',
        '222222',
        '333333',
        '444444',
        '555555',
        '666666',
        '777777',
        '888888',
        '999999',
        '012345',
        '123456',
        '234567',
        '345678',
        '456789',
        '567890',
        '098765',
        '987654',
        '876543',
        '765432',
        '654321',
        '543210'
    ]

    try:
        if preserve_pin:
            pin = currentPin(vin)

        if (pin is None):
            # generate 6 digit PIN
            pin = generatePin()

        # recursive to generate a pin until you get one that is allowed
        if pin in disallowedPins:
            factory_pin_generate(vin)

        # save pin to authority manager db
        insert_into_vehicle_meta_table(vin, 'pin', 'factory_pin', pin)

        result['pin'] = pin

        return result

    except Exception as e:
        logger.exception(f'Failed to execute factory_pin_generate for {vin}')
        raise e


# get the PIN already in auth
def currentPin(vin):
    cursor = None
    pin = None
    try:
        cursor = arcimoto.db.get_cursor()
        args = [vin, 'pin', 'factory_pin']
        query = (
            'SELECT value '
            'FROM vehicle_meta '
            'WHERE vin=%s AND section=%s AND key=%s'
        )
        cursor.execute(query, args)
        for row in cursor:
            pin = row['value']
        cursor.close()
    except Exception as e:
        logger.exception(f'Error: There was a problem retrieving the factory pin for {vin}')
        raise ArcimotoException(f'Error: There was a problem retrieving the factory pin for {vin}: {e}')
    return pin


# insert into vehicle_meta table
def insert_into_vehicle_meta_table(vin, section, key, value):
    '''
    Creates a new entry in vehicle_meta table, uses (vin, section, key) as primary id
    '''

    conn = None
    cursor = None

    reserved_keys = ['vin', 'groups', 'telemetry']
    if section in reserved_keys:
        raise Exception('Attempt to set meta section to reserved value: {}'.format(section))

    cursor = arcimoto.db.get_cursor()
    query = (
        'INSERT INTO vehicle_meta '
        '(vin, section, key, value) VALUES (%s, %s, %s, %s) '
        'ON CONFLICT (vin, section, key) DO UPDATE SET value = %s '
        'RETURNING vin, section, key, value'
    )
    cursor.execute(query, [vin, section, key, value, value])
    returned_from_db = cursor.fetchone()
    logger.debug('(vin, section, key, value) = ({}, {}, {}, {}) exists in the vehicle_meta table'.format(returned_from_db[0], returned_from_db[1], returned_from_db[2], returned_from_db[3]))
    return {}


def generatePin():
    return str(random.randint(1, 1000000)).zfill(6)


lambda_handler = factory_pin_generate
