import logging
import copy
from datetime import datetime, timedelta

from arcimoto.exceptions import *
import arcimoto.runtime
import arcimoto.args
import arcimoto.user
import arcimoto.db

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

arcimoto.args.register({
    'vehicles_db_data': {
        'type': 'dict'
    },
    'vehicles_telemetry_data': {
        'type': 'list',
        'empty': False
    }
})


@arcimoto.runtime.handler
def yrisk_output_assemble(vehicles_db_data, vehicles_telemetry_data):
    global logger

    try:
        (last_month_start, last_month_end) = get_last_month_timestamps()

        last_month_start_timestamp = last_month_start.timestamp()
        start_milliseconds = f'{int(last_month_start_timestamp * 1000)}ms'

        last_month_end_timestamp = last_month_end.timestamp()
        end_milliseconds = f'{int(last_month_end_timestamp * 1000)}ms'
    except Exception as e:
        raise ArcimotoYRiskAlertException(f'Unable to setup telemetry point period: {e}')

    output = {
        'start': arcimoto.db.datetime_record_output(last_month_start),
        'end': arcimoto.db.datetime_record_output(last_month_end),
        'vehicles': copy.deepcopy(vehicles_db_data.get('vehicles'))
    }

    # add vehicle telemetry data to db data
    for vehicle in output.get('vehicles', []):
        vin = vehicle.get('vin')
        vehicle_telemetry = next(item for item in vehicles_telemetry_data if item['vin'] == vin)
        vehicle_odometer = vehicle_telemetry.get('odometer', [])
        vehicle['telemetry'] = {
            'odometer': {
                'start': vehicle_odometer[0],
                'end': vehicle_odometer[1] if len(vehicle_odometer) > 1 else vehicle_odometer[0]
            } if len(vehicle_odometer) else 'unknown'
        }

    return output


def get_last_month_timestamps():
    try:
        current_month = datetime.now().month
        current_year = datetime.now().year
        this_month_start = datetime(current_year, current_month, 1)

        last_month = current_month - 1 if current_month > 1 else 12
        last_month_year = current_year if current_month > 1 else current_year - 1

        last_month_start = datetime(last_month_year, last_month, 1)
        last_month_end = this_month_start - timedelta(seconds=1)
    except Exception as e:
        raise ArcimotoYRiskAlertException(f'Unable to get last month timestamps: {e}')

    return (last_month_start, last_month_end)


lambda_handler = yrisk_output_assemble
