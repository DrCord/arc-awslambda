import logging

from arcimoto.exceptions import *
import arcimoto.runtime
import arcimoto.args
import arcimoto.note

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

arcimoto.args.register({
    'json_data': {
        'type': 'dict'
    }
})


@arcimoto.runtime.handler
def yrisk_notify(json_data):
    global logger

    vins_missing_odometer_readings = []

    for vehicle in json_data.get('vehicles'):
        vehicle_telemetry = vehicle.get('telemetry')
        if vehicle_telemetry.get('odometer') == 'unknown':
            vins_missing_odometer_readings.append(vehicle.get('vin'))

    date_range = f'[{json_data.get("start")} - {json_data.get("end")}]'

    # notification for vins without odometer readings
    try:
        msg_lines = [
            'Y-Risk Telemetry Data Issue',
            'Vehicles Missing Odometer Readings',
            date_range
        ]
        msg = '\n'.join(msg_lines) + f'\n\n' + "\n".join(vins_missing_odometer_readings)

        arcimoto.note.YRiskNotification(
            message=msg,
            source='Y-Risk-Monthly-Vehicle-Telemetry',
            source_type='state_machine',
            data={},
            severity='WARNING'
        )

        arcimoto.note.ServiceNotification(
            message=msg,
            source='Y-Risk-Monthly-Vehicle-Telemetry',
            source_type='state_machine',
            data={},
            severity='WARNING'
        )
    except Exception as e:
        logger.warning(f'Failed to send vehicles missing odometer readings notification: {e}')

    # notification for completion
    try:
        msg_lines = [
            'Y-Risk Data Output Complete',
            date_range
        ]
        msg = '\n'.join(msg_lines)
        arcimoto.note.YRiskNotification(
            message=msg,
            source='Y-Risk-Monthly-Vehicle-Telemetry',
            source_type='state_machine',
            data={},
            severity='INFO'
        )
    except Exception as e:
        logger.warning(f'Failed to send yrisk data output complete notification: {e}')

    return {}


lambda_handler = yrisk_notify
