import logging

from arcimoto.exceptions import *
import arcimoto.args
import arcimoto.db
import arcimoto.note
import arcimoto.runtime
import arcimoto.user

import firmware as firmware_class
import parts as parts_class

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

arcimoto.args.register({
    'vin': {
        'type': 'string',
        'required': True
    },
    'data': {
        'type': 'dict',
        'required': True
    }
})


@arcimoto.runtime.handler
@arcimoto.db.transaction
def register_vehicle(vin, data):
    '''
    This should only be run on an already existing vehicle.
    If the vehicle does not exist, throw an error message.

    - sets parts for vehicle from vehicle->model_release parts
    - creates vehicle note with initial parts
    - sets firmware for vehicle from latest master hashes in db
    - create vehicle note with initial firmware
    - posts notification

    Attached to IoT Act rule for each ENV.
    IoT rule names: {ENV}_vehicle_registration
    '''
    global logger

    firmware_resources = firmware_class.Firmware()
    parts_resources = parts_class.Parts(None, vin)
    vehicle_instance = arcimoto.vehicle.Vehicle(vin)
    if not vehicle_instance.exists:
        raise ArcimotoNotFoundError(f'Invalid: no provisioned vehicle for vin {vin}: unable to register vehicle.')

    # handle discoboard mismatch in registration data board number and model release
    board = None
    registration_indicates_discoboard = None

    for key, value in data.items():
        keyParts = key.split(':')
        # registration
        if len(keyParts) == 1:
            if key == 'board':
                board = value
    if board is None:
        logger.warning(f'No board in input payload: {data}')
    else:
        registration_indicates_discoboard = True if board == 1105 else False
    if registration_indicates_discoboard is None:
        logger.warning(f'Unable to determine vehicle discoboard status from payload: {data}')
    for part_type, part_number in parts_resources.model_release_parts.items():
        if part_type == 'Comm':
            part_number_indicates_discoboard = part_number == '004280'
            if registration_indicates_discoboard != part_number_indicates_discoboard:
                msg = f'Discoboard mismatch for {vin}: Registration data and part from model release do not match. Model Release Comm part number {part_number}, Registration board id: {board}.'
                arcimoto.note.ServiceNotification(
                    message=msg,
                    source='register_vehicle',
                    data={},
                    severity=arcimoto.note.SEVERITY_ERROR
                )
                raise ArcimotoManufacturingAlertException(msg)

    for key, value in data.items():
        keyParts = key.split(':')
        if len(keyParts) == 1:
            args = ['registration', key, value]
        else:
            args = [keyParts[0], keyParts[1], value]
        vehicle_instance.update_meta(*args)
    # set parts for vehicle from vehicle->model_release parts
    try:
        for part_type in parts_resources.model_release_parts:
            try:
                parts_resources.vehicle_part_install(vin, part_type)
            except Exception as e:
                logger.warning(f'Failure to install {part_type} for {vin}: {e}')
    except Exception as e:
        logger.warning(f'Failure to install parts for {vin}: {e}')

    try:
        msg_parts = 'Initial Parts Set:\n{}'.format('\n'.join('{}: {}'.format(k, i) for k, i in parts_resources.vehicle_parts.items()))
        arcimoto.note.VehicleNote(
            vin=vin,
            message=msg_parts,
            tags=['parts']
        )
    except Exception as e:
        logger.warning(f'Failed to set initial parts note for {vin}: {e}')

    # firmware
    try:
        # gets latest master hashes stored in db
        firmware_version_get_response = firmware_resources.firmware_version_get()
        release_firmware_module_hashes = firmware_version_get_response.get('firmware', None)
        if release_firmware_module_hashes is None:
            raise ArcimotoException('firmware_version_get: unable to get release module data')
    except Exception as e:
        logger.warning('Failed to retrieve firmware data. Invoking firmware_version getter lambda failed: {}'.format(e))

    try:
        # sets hashes in db from vehicle
        update = firmware_resources.firmware_version_vin_set(vin, release_firmware_module_hashes)
    except Exception as e:
        logger.warning('Failed to capture firmware data. Invoking firmware_version setter lambda failed: {}'.format(e))

    try:
        updated_firmware_original = update.get('updated_firmware', {})
        if '004280 Comm Bootloader' in updated_firmware_original:
            del updated_firmware_original['004280 Comm Bootloader']
        if '004280 Comm Firmware' in updated_firmware_original:
            del updated_firmware_original['004280 Comm Firmware']
        updated_firmware = []
        for k, i in updated_firmware_original.items():
            updated_firmware.append({
                'firmware_component': k,
                'hash': i,
            })
        msg_firmware = 'Initial Firmware Versions Set:\n{}'.format('\n'.join('{}: {}'.format(item['firmware_component'], item['hash']) for item in sorted(updated_firmware, key=lambda x: x['firmware_component'])))
        arcimoto.note.VehicleNote(
            vin=vin,
            message=msg_firmware,
            tags=['firmware']
        )
    except Exception as e:
        logger.warning(f'Failed to set initial firmware versions note for {vin}: {e}')

    # notification
    try:
        msg = f'{vin} registered\n\n{msg_firmware}\n\n{msg_parts}'
        arcimoto.note.ManufacturingNotification(
            message=msg,
            source='register_vehicle',
            data={},
            severity='INFO'
        )
        arcimoto.note.ServiceNotification(
            message=msg,
            source='register_vehicle',
            data={},
            severity='INFO'
        )
    except Exception as e:
        logger.warning(f'Failed to send registration notification for {vin}: {e}')

    return {}


lambda_handler = register_vehicle
