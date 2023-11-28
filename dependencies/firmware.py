import json
import logging
import certifi
import urllib3

from arcimoto.exceptions import *
import arcimoto.db
import arcimoto.note
import arcimoto.runtime
import arcimoto.vehicle

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class Firmware:

    TOKEN_URL = "https://bitbucket.org/site/oauth2/access_token"
    REQUEST_URL = "https://api.bitbucket.org/2.0/repositories/arcimotocode1/"

    FIRMWARE = {
        'BMS Firmware.o2bx': 'BMS Firmware',
        'BMS Profile.o2bms': 'BMS Profile',
        'Comm Bootloader.dfu': 'Comm Bootloader',
        'Comm Firmware.dfu': 'Comm Firmware',
        'Display Bootloader.dfu': 'Display Bootloader',
        'Display Firmware.dfu': 'Display Firmware',
        'EPSU Application.hex': 'EPSU Application',
        'EPSU Firmware.hex': 'EPSU Firmware',
        'EPSU Profile.cal': 'EPSU Profile',
        'Front IO Firmware.s19': 'IO Firmware - Front',
        'H Bridge Firmware.s19': 'H Bridge Firmware',
        'Inverter Profile Left.clon': 'Inverter Profile - Left',
        'Inverter Profile Right.clon': 'Inverter Profile - Right',
        'LV Bootloader.dfu': 'LV Bootloader',
        'LV Firmware.dfu': 'LV Firmware',
        'Rear IO Firmware.s19': 'IO Firmware - Rear',
        'TAUSYS_SY_AM2.': 'Inverter Firmware',
        'VCU Firmware.srec': 'VCU Firmware',
        'Comm Option Bytes.dfu': 'Comm Option Bytes',
        'Display Option Bytes.dfu': 'Display Option Bytes',
        'LV Option Bytes.dfu': 'LV Option Bytes'
    }

    bitbucket_access_token = None

    FIRMWARE_IDENTIFIER_COMM_BOOTLOADER_DISCOBOARD = '004280 Comm Bootloader'
    FIRMWARE_IDENTIFIER_COMM_FIRMWARE_DISCOBOARD = '004280 Comm Firmware'

    @property
    def bb_token(self):
        return self.bitbucket_access_token if self.bitbucket_access_token is not None else self.get_auth_token()

    @property
    def bb_api_call_headers(self):
        return {'Authorization': 'Bearer ' + self.bb_token}

    def __init__(self):
        super().__init__()

    def get_auth_token(self):
        """Get OAuth2 token for bitbucket using consumer key and password"""

        credentials = arcimoto.runtime.get_secret('bitbucket.oauth2.lambda.firmware.read')
        data = {
            'grant_type': 'client_credentials'
        }
        credentials_string = credentials['key'] + ':' + credentials['secret']
        headers = urllib3.make_headers(basic_auth=credentials_string)

        # recommended to do ssl verification for requests
        # https://urllib3.readthedocs.io/en/latest/user-guide.html#ssl
        http = urllib3.PoolManager(
            cert_reqs='CERT_REQUIRED',
            ca_certs=certifi.where()
        )
        access_token_response = http.request(
            'POST',
            self.TOKEN_URL,
            fields=data,
            headers=headers
        )
        json_response = json.loads(access_token_response.data.decode('utf-8'))

        self.bitbucket_access_token = json_response.get('access_token', None)

        return json_response.get('access_token', None)

    def get_commit_info(self, token, repo, firmware=None):
        """Get of latest master commit of provided repo name and firmware in ArcimotoCode"""

        api_call_headers = {'Authorization': 'Bearer ' + token}

        try:
            env = arcimoto.runtime.get_env()
            if env is arcimoto.runtime.ENV_PROD:
                branch = 'master'
            else:
                branch = env
            request_path = f'{self.REQUEST_URL}{repo}/commits/{branch}'

            if firmware:
                request_path += '?'
                request_path += f'path={firmware.replace(" ", "%20")}'
        except Exception as e:
            raise ArcimotoException(f'Unable to create request_path: error: {e}') from e

        try:
            # recommended to do ssl verification for requests
            # https://urllib3.readthedocs.io/en/latest/user-guide.html#ssl
            http = urllib3.PoolManager(
                cert_reqs='CERT_REQUIRED',
                ca_certs=certifi.where()
            )
            api_call_response = http.request(
                'GET',
                request_path,
                headers=api_call_headers
            )
        except Exception as e:
            raise ArcimotoException(f'Unable to complete urllib3 http GET request for commit info - error: {e}') from e

        try:
            json_response = json.loads(api_call_response.data.decode('utf-8'))
            json_response_list = json_response.get('values', [])
            json_response_item = json_response_list[0] if len(json_response_list) else {}
        except Exception as e:
            raise ArcimotoException(f'Unable to parse json response - error: {e}') from e

        return {
            'hash': json_response_item.get('hash', ''),
            'author': json_response_item.get('author', {}).get('raw', ''),
            'date': json_response_item.get('date', ''),
            'message': json_response_item.get('message', '').replace('\n', '')
        }

    def firmware_version_get(self, firmware_modules_input=None):
        '''Gets most recent version hash for each firmware_component requested or all'''
        cursor = arcimoto.db.get_cursor()
        firmware = {}
        query_start = (
            'SELECT firmware_component, hash '
            'FROM firmware_release '
        )
        query_where = 'WHERE firmware_component = %s '
        query_order = 'ORDER BY created DESC, firmware_component ASC, firmware_release_id DESC '
        query_limit = 'LIMIT 1'

        if firmware_modules_input is not None and type(firmware_modules_input) is dict:
            for firmware_component, hash in firmware_modules_input.items():
                # this allows you to force the input value to be the output value
                if hash is not None:
                    firmware[firmware_component] = hash
                else:
                    query = query_start + query_where + query_order + query_limit
                    cursor.execute(query, [firmware_component])
                    result = cursor.fetchone()
                    hash = result.get('hash', None)
                    if hash is None:
                        logger.warning(f'Unable to get hash for {firmware_component}')
                    firmware[firmware_component] = hash
        else:
            query = query_start + query_order
            cursor.execute(query)
            for record in cursor:
                firmware_component = record['firmware_component']
                hash = record['hash']
                if firmware_component not in firmware:
                    firmware[firmware_component] = hash

        return {'firmware': firmware}

    @arcimoto.db.transaction
    def firmware_version_vin_set(self, vin, firmware_components):
        firmware_updates = {}
        firmware_components_mapped_to_part_type = {}
        vehicle_has_discoboard = None

        query_select_part_types = (
            'SELECT part_type, firmware_component '
            'FROM firmware_components'
        )
        query_select_firmware_release_id = (
            'SELECT firmware_release_id '
            'FROM firmware_release '
            'WHERE firmware_component = %s '
            'ORDER BY created DESC, firmware_release_id DESC LIMIT 1'
        )
        query_insert = (
            'INSERT INTO vehicle_firmware_installed '
            '(vin, part_type, firmware_component, firmware_release_id) '
            'VALUES (%s, %s, %s, %s) '
            'ON CONFLICT ON CONSTRAINT vehicle_firmware_installed_pkey DO UPDATE '
            'SET installed = NOW(), '
            'firmware_release_id = excluded.firmware_release_id'
        )

        cursor = arcimoto.db.get_cursor()

        try:
            # lookup part_types - get firmware_components data into lookup dict
            # firmware component -> [part_types]
            cursor.execute(query_select_part_types)
            for record in cursor.fetchall():
                if firmware_components_mapped_to_part_type.get(record['firmware_component'], None) is None:
                    firmware_components_mapped_to_part_type[record['firmware_component']] = []
                firmware_components_mapped_to_part_type[record['firmware_component']].append(record['part_type'])
        except Exception as e:
            raise ArcimotoException(f'Failure to lookup map of firmware_components to part_types: {e}')

        # remove "Deployed Firmware" so we don't insert it later
        if 'Deployed Firmware' in firmware_components:
            del firmware_components['Deployed Firmware']

        # handle exceptions for part_number prefixed firmware_components
        if firmware_components_mapped_to_part_type.get('Inverter Profile - Left', None) is not None:
            firmware_components_mapped_to_part_type['001325 Inverter Profile Left'] = firmware_components_mapped_to_part_type['Inverter Profile - Left']
            firmware_components_mapped_to_part_type['001412 Inverter Profile Left'] = firmware_components_mapped_to_part_type['Inverter Profile - Left']
        if firmware_components_mapped_to_part_type.get('Comm Bootloader', None) is not None:
            firmware_components_mapped_to_part_type[self.FIRMWARE_IDENTIFIER_COMM_BOOTLOADER_DISCOBOARD] = firmware_components_mapped_to_part_type['Comm Bootloader']
        if firmware_components_mapped_to_part_type.get('Comm Firmware', None) is not None:
            firmware_components_mapped_to_part_type[self.FIRMWARE_IDENTIFIER_COMM_FIRMWARE_DISCOBOARD] = firmware_components_mapped_to_part_type['Comm Firmware']

        # get vin part_number installed info from model_release_id
        parts_query = (
            'SELECT vmp.part_type, vmp.part_number '
            'FROM vehicle_model_parts vmp '
            'JOIN vehicle v ON v.model_release_id = vmp.model_release_id '
            'WHERE vin = %s'
        )
        vehicle_parts = {}
        try:
            cursor.execute(parts_query, [vin])
            result = cursor.fetchall()
            if result is not None:
                for item in result:
                    vehicle_parts[item['part_type']] = item['part_number']
        except Exception as e:
            raise ArcimotoException(f'Failure vin {vin} => parts lookup: {e}')

        # handle exception firmware_components due to prefix in full firmware list
        # use vehicle_parts (part_type->part_numbers) to select correct firmware_component to get hash from
        # Discoboard
        if 'Comm Bootloader' in firmware_components or 'Comm Firmware' in firmware_components:
            comm_part_number = vehicle_parts.get('Comm', None)
            if comm_part_number is None:
                raise ArcimotoException(f'Failure vin {vin} => part lookup for Comm')
            vehicle_has_discoboard = True if comm_part_number == '004280' else False
            # select correct firmware_component and remove the others related
            if vehicle_has_discoboard:
                if (
                    'Comm Bootloader' in firmware_components and
                    self.FIRMWARE_IDENTIFIER_COMM_BOOTLOADER_DISCOBOARD in firmware_components
                ):
                    firmware_components['Comm Bootloader'] = firmware_components[self.FIRMWARE_IDENTIFIER_COMM_BOOTLOADER_DISCOBOARD]
                if (
                    'Comm Firmware' in firmware_components and
                    self.FIRMWARE_IDENTIFIER_COMM_FIRMWARE_DISCOBOARD in firmware_components
                ):
                    firmware_components['Comm Firmware'] = firmware_components[self.FIRMWARE_IDENTIFIER_COMM_FIRMWARE_DISCOBOARD]
        if self.FIRMWARE_IDENTIFIER_COMM_BOOTLOADER_DISCOBOARD in firmware_components:
            del firmware_components[self.FIRMWARE_IDENTIFIER_COMM_BOOTLOADER_DISCOBOARD]
        if self.FIRMWARE_IDENTIFIER_COMM_FIRMWARE_DISCOBOARD in firmware_components:
            del firmware_components[self.FIRMWARE_IDENTIFIER_COMM_FIRMWARE_DISCOBOARD]
        # KERS Sensor update
        if 'Inverter Profile - Left' in firmware_components:
            kers_sensor_part_number = vehicle_parts.get('KERS Sensor', None)
            if kers_sensor_part_number is None:
                raise ArcimotoException(f'Failure vin {vin} => parts lookup for KERS Sensor')
            # select correct firmware_component and remove the others related
            if f'{kers_sensor_part_number} Inverter Profile Left' in firmware_components:
                firmware_components['Inverter Profile - Left'] = firmware_components[f'{kers_sensor_part_number} Inverter Profile Left']
        if '001325 Inverter Profile Left' in firmware_components:
            del firmware_components['001325 Inverter Profile Left']
        if '001412 Inverter Profile Left' in firmware_components:
            del firmware_components['001412 Inverter Profile Left']

        try:
            for firmware_component, hash in firmware_components.items():
                try:
                    # handle IO Front/Rear mismatch
                    if firmware_component in ['IO Firmware - Front', 'IO Firmware - Rear']:
                        firmware_component = f"{firmware_component.replace('Firmware - ', '')} Profile"
                    # lookup firmware_release_id
                    # handle KERS Sensor Inverter - Left split
                    if firmware_component == 'Inverter Profile - Left':
                        cursor.execute(query_select_firmware_release_id, [f'{kers_sensor_part_number} Inverter Profile Left'])
                    elif firmware_component in ['Comm Bootloader', 'Comm Firmware'] and vehicle_has_discoboard:
                        # Exception for the Discoboard (part number 004280)
                        cursor.execute(query_select_firmware_release_id, [f'004280 {firmware_component}'])
                    else:
                        cursor.execute(query_select_firmware_release_id, [firmware_component])
                    result = cursor.fetchone()
                    if result is None:
                        raise ArcimotoException(f'No firmware_release_id found for {firmware_component}')
                    firmware_release_id = result.get('firmware_release_id')
                except Exception as e:
                    raise ArcimotoException(f'Failure of select query to lookup firmware_release_id: {e}')
                # get part_type for the firmware_component
                try:
                    part_types = self.vehicle_part_type_get(firmware_component, firmware_components_mapped_to_part_type)
                    if not part_types:
                        raise ArcimotoException(f'part_type(s) not available, firmware_component: {firmware_component}, vin: {vin}')
                except Exception as e:
                    raise ArcimotoException(f'Failure firmware_component => part_type lookup: {e}')
                # insert records
                for part_type in part_types:
                    try:
                        args = [
                            vin,
                            part_type,
                            firmware_component,
                            firmware_release_id
                        ]
                        if 'Invalid' in hash:
                            args[3] = None
                        cursor.execute(query_insert, args)
                    except Exception as e:
                        raise ArcimotoException(f'Failure of insert query for {vin}:{part_type}:{firmware_component} - {e}')
                    try:
                        msg_firmware = 'Firmware Set:\n{} - firmware release id: {}'.format(firmware_component, firmware_release_id)
                        arcimoto.note.VehicleNote(
                            vin=vin,
                            message=msg_firmware,
                            tags=['firmware']
                        )
                    except Exception as e:
                        raise ArcimotoException(f'Failure to create vehicle note for {vin}:{part_type}:{firmware_component} - {e}')

                firmware_updates[firmware_component] = hash

            return {'updated_firmware': firmware_updates}

        except Exception as e:
            # Note: the CloudWatch Alarm 'Firmware version vin set failed'
            # depends on the text 'firmware_version_vin_set failed' appearing in the next message:
            logger.exception('firmware_version_vin_set failed')
            raise ArcimotoException(e)

    def vehicle_part_type_get(self, firmware_component, firmware_components_mapped_to_part_type):
        # handle exceptions due to prefix of part number
        exceptions = {
            '001325 Inverter Profile Left': 'Inverters',
            '001412 Inverter Profile Left': 'Inverter - Left',
            self.FIRMWARE_IDENTIFIER_COMM_BOOTLOADER_DISCOBOARD: 'Comm',
            self.FIRMWARE_IDENTIFIER_COMM_FIRMWARE_DISCOBOARD: 'Comm'
        }
        if firmware_component in exceptions.keys():
            part_types = [exceptions.get(firmware_component)]
        # get non-exception part_types directly from mapping dict
        else:
            part_types = firmware_components_mapped_to_part_type.get(firmware_component, None)
        return part_types
