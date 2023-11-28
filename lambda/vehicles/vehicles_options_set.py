import logging

from arcimoto.exceptions import *
import arcimoto.runtime
import arcimoto.args
import arcimoto.user
import arcimoto.vehicle

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

arcimoto.args.register({
    'vin': {
        'type': 'string',
        'required': True
    },
    'options': {
        'type': 'dict',
        'required': True,
        'empty': False
    }
})

OPTION_KEYS = {
    'heated_seats': 'heated_seats',
    'heated_grips': 'heated_grips',
    'stereo_enabled': 'stereo_enabled'
}

OPTION_SECTION = 'options'


@arcimoto.runtime.handler
@arcimoto.user.require('vehicles.vehicle.write')
def vehicles_options_set(vin, options):
    global logger

    vehicle_instance = arcimoto.vehicle.Vehicle(vin)

    for option_key in options:
        key = OPTION_KEYS.get(option_key, None)
        if key is not None:
            vehicle_instance.update_meta(OPTION_SECTION, key, options.get(key))

    return {}


lambda_handler = vehicles_options_set
