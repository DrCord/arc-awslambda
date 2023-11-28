import logging

from arcimoto.exceptions import *
import arcimoto.runtime
import arcimoto.user

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


@arcimoto.runtime.handler
@arcimoto.user.require('telemetry.points.read')
def telemetry_points_get_defaults():
    telemetry_points = {
        'ambient_temp': {},
        'bms_multi_purpose_enable': {},
        'bms_pack_ccl': {},
        'bms_pack_current': {},
        'bms_pack_dcl': {},
        'bms_pack_instantaneous_voltage': {},
        'bms_pack_soc': {},
        'controller_1_inverter_temperature': {},
        'controller_1_motor_temperature': {},
        'controller_2_inverter_temperature': {},
        'controller_2_motor_temperature': {},
        'gps_altitude': {},
        'gps_position': {},
        'lv_voltage_1': {},
        'odometer': {},
        'speed': {}
    }

    return {'telemetry_points': telemetry_points}


lambda_handler = telemetry_points_get_defaults
