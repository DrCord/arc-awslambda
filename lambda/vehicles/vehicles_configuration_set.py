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
    'configuration': {
        'type': 'dict',
        'required': True,
        'empty': False
    }
})

CONFIGURATION_KEYS = {
    'option_governor_max_speed': 'option_governor_max_speed'
}

CONFIGURATION_SECTION = 'configuration'


@arcimoto.runtime.handler
@arcimoto.user.require('vehicles.vehicle.configuration_write')
def vehicles_configuration_set(vin, configuration):
    global logger

    vehicle_instance = arcimoto.vehicle.Vehicle(vin)

    for configuration_key in configuration:
        key = CONFIGURATION_KEYS.get(configuration_key, None)
        if key is not None:
            vehicle_instance.update_meta(CONFIGURATION_SECTION, key, configuration.get(key))

    return {}


lambda_handler = vehicles_configuration_set
