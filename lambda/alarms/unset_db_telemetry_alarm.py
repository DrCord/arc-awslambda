import logging

from arcimoto.exceptions import *
import arcimoto.db
import arcimoto.runtime
import arcimoto.vehicle

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

arcimoto.args.register({
    'vin': {
        'type': 'string',
        'required': True,
        'empty': False
    },
    'set_alarm': {
        'type': 'boolean',
        'default': False
    }
})

@arcimoto.runtime.handler
def unset_db_telemetry_alarm_handler(vin, set_alarm):
    try:
        tf = {True: True, False: False}
        return unset_db_telemetry_alarm(vin, tf[set_alarm])

    except Exception as e:
        logger.exception(f"unset_db_telemetry_alarm lambda failed: {e}")
        raise Exception(f"Unset Vehicle Telemetry Alarm failed: {e}")


lambda_handler = unset_db_telemetry_alarm_handler


def unset_db_telemetry_alarm(vin, set_alarm):
    """
    This should only be run on an already existing vehicle.
    If the vehicle does not exist, throw an error message.
    """

    # alarm metadata
    registration = {}
    registration["telemetry rate"] = set_alarm

    # Instantiate vehicle instance
    vehicle = arcimoto.vehicle.Vehicle(vin)
    try:
        for key, value in registration.items():
            vehicle.update_meta("alarms", key, value)

    except Exception as e:
        logger.warning(f"Failed to update telemetry alarm db entry: {e}")

    return {}
