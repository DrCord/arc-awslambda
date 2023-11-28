import logging

from arcimoto.exceptions import *
import arcimoto.runtime
import arcimoto.user
import arcimoto.db

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


@arcimoto.runtime.handler
@arcimoto.user.require('vehicles.vehicle.read')
def vehicles_firmware_components_list():
    global logger

    cursor = arcimoto.db.get_cursor()

    query = (
        'SELECT part_type, firmware_component, created '
        'FROM firmware_components'
    )
    firmware_components = []

    cursor.execute(query)
    for record in cursor:
        firmware_components.append(
            {
                'part_type': record['part_type'],
                'firmware_component': record['firmware_component'],
                'created': arcimoto.db.datetime_record_output(record['created'])
            }
        )
    return {'firmware_components': firmware_components}


lambda_handler = vehicles_firmware_components_list
