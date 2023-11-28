import logging

from arcimoto.exceptions import *
import arcimoto.runtime
import arcimoto.user
import arcimoto.db

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

arcimoto.args.register({
    'vin': {
        'type': 'string',
        'required': True
    }
})


@arcimoto.runtime.handler
@arcimoto.user.require('firmware.vehicle.read')
def firmware_version_vin_get(vin):
    global logger
    cursor = arcimoto.db.get_cursor()

    if vehicle_exists(vin) is False:
        raise ArcimotoArgumentError('vin {} does not exist'.format(vin))

    firmware = []
    query = (
        'SELECT vfi.part_type, vfi.firmware_component, vfi.firmware_release_id, vfi.installed, fr.hash '
        'FROM vehicle_firmware_installed AS vfi '
        'JOIN firmware_release as fr ON vfi.firmware_release_id=fr.firmware_release_id '
        'WHERE vfi.vin = %s '
        'ORDER BY vfi.part_type, vfi.firmware_component ASC'
    )
    cursor.execute(query, [vin])
    for record in cursor.fetchall():
        item = {
            'part_type': record['part_type'],
            'firmware_component': record['firmware_component'],
            'firmware_release_id': record['firmware_release_id'],
            'installed': arcimoto.db.datetime_record_output(record['installed']),
            'hash': record['hash']
        }
        firmware.append(item)

    firmware_versions = {}
    for firmware_item in firmware:
        firmware_versions[firmware_item['firmware_component']] = firmware_item['hash']
    logger.debug(f'vehicle firmware: {firmware_versions}')

    return firmware_versions


def vehicle_exists(vin):
    return arcimoto.db.check_record_exists('vehicle', {'vin': vin})


lambda_handler = firmware_version_vin_get
