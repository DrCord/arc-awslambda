import base64
import json
import logging

from arcimoto.exceptions import *
import arcimoto.runtime
import arcimoto.user
import arcimoto.db

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

arcimoto.args.register({
    'firmware': {
        'type': 'dict',
        'required': True
    }
})


@arcimoto.runtime.handler
@arcimoto.db.transaction
def firmware_version_set_release_data(firmware):
    """Sets a version hash in the meta and firmware_release tables for each firmware_component"""
    # Note: the CloudWatch Alarm "New Firmware Version Hash Set - prod"
    # depends on the text "prod env" appearing in the next message:
    logger.info('Calling firmware_version_set_release_data with {} env'.format(arcimoto.runtime.get_env()))

    cursor = arcimoto.db.get_cursor()
    firmware_updates = {}
    meta_query = (
        'INSERT INTO meta '
        '(section, key, value) '
        'VALUES (%s, %s, %s) '
        'ON CONFLICT (section, key) '
        'DO UPDATE SET value = excluded.value '
        'RETURNING section, key, value'
    )
    vehicle_firmware_release_query = (
        'INSERT INTO firmware_release '
        '(part_type, firmware_component, description, hash) '
        'VALUES (%s, %s, %s, %s) '
        'ON CONFLICT ON CONSTRAINT firmware_release_part_type_firmware_component_hash_key DO NOTHING'
    )
    firmware_versions_query = (
        'INSERT INTO firmware_versions '
        '(firmware_component, hash) '
        'VALUES (%s, %s) '
        'ON CONFLICT ON CONSTRAINT firmware_versions_pkey DO NOTHING'
    )
    parts_query = (
        'SELECT part_type '
        'FROM firmware_components '
        'WHERE firmware_component = %s'
    )

    try:
        for item, meta in firmware.items():
            firmware_component = meta['name']
            description = meta['message']
            hash = meta['hash']
            if firmware_component == 'Charger Firmware':
                continue

            # overwrite existing old data in deprecated data store in meta table
            cursor.execute(meta_query, ['firmware', firmware_component, hash])

            # create data in vehicle release data store
            # insert into list of all possible hashes for a firmware component
            cursor.execute(firmware_versions_query, [firmware_component, hash])

            # leave out "Deployed Firmware" holistic (overall) firmware hash in new data store
            if firmware_component != 'Deployed Firmware':
                if firmware_component == 'IO Firmware - Front' or firmware_component == 'IO Firmware - Rear':
                    firmware_component = f"{firmware_component.replace('Firmware - ', '')} Profile"

                part_types = []
                cursor.execute(parts_query, [firmware_component])
                result = cursor.fetchall()
                if result is not None:
                    for item in result:
                        part_types.append(item['part_type'])
                # if no part_types: supply from exceptions
                if not len(part_types):
                    if firmware_component == '001325 Inverter Profile Left':
                        part_types.append('Inverters')
                    elif firmware_component == '001412 Inverter Profile Left':
                        part_types.append('Inverter - Left')
                    elif firmware_component == '004280 Comm Bootloader':
                        part_types.append('Comm')
                    elif firmware_component == '004280 Comm Firmware':
                        part_types.append('Comm')
                # raise exception if still doesn't have part type after exceptions handling above
                if not len(part_types):
                    raise ArcimotoException(f'No part_type(s) available for firmware component {firmware_component}')
                # insert firmware_release data for each firmware_component:part_type combination
                for part_type in part_types:
                    cursor.execute(vehicle_firmware_release_query, [part_type, firmware_component, description, hash])

            # Note: the CloudWatch Alarm "New Firmware Version Hash Set - prod"
            # depends on the text"Inserted hash" appearing in the next message:
            logger.info('Inserted hash {} for {}'.format(hash, firmware_component))
            firmware_updates[firmware_component] = hash
    except Exception as e:
        raise ArcimotoFirmwareAlertException(e)

    firmware_updates_sorted = {}
    for i in sorted(firmware_updates.keys(), key=lambda x: x.lower()):
        firmware_updates_sorted[i] = firmware_updates.get(i)

    msg_firmware = 'Release Firmware Versions Set:\n{}'.format('\n'.join('{}: {}'.format(firmware_component_name, hash) for firmware_component_name, hash in firmware_updates_sorted.items()))
    msg = f'Firmware Release Versions Set\n\n{msg_firmware}'
    # output into firmware, manufacturing and service notification channels
    arcimoto.note.FirmwareNotification(
        message=msg,
        source='firmware_version_set_release_data',
        data={},
        severity='INFO'
    )
    arcimoto.note.ManufacturingNotification(
        message=msg,
        source='firmware_version_set_release_data',
        data={},
        severity='INFO'
    )
    arcimoto.note.ServiceNotification(
        message=msg,
        source='firmware_version_set_release_data',
        data={},
        severity='INFO'
    )

    return {'updated_firmware': firmware_updates_sorted}


lambda_handler = firmware_version_set_release_data
