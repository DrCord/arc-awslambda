import logging

from arcimoto.exceptions import *
import arcimoto.db
import arcimoto.runtime
import arcimoto.vehicle

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class Parts:

    _vehicles_part_types_available = []
    _model_release_parts = {}
    _vehicle_parts = {}
    _MODEL_RELEASE_ID = None
    _VIN = None

    def __init__(self, model_release_id=None, vin=None):
        super().__init__()
        self._MODEL_RELEASE_ID = model_release_id
        if vin is not None:
            vehicle = arcimoto.vehicle.Vehicle(vin)
            if not vehicle.exists:
                raise ArcimotoNotFoundError(f'Invalid vin: {vin}')
        self._VIN = vin
        if self._MODEL_RELEASE_ID is None and self._VIN is not None:
            self.vehicle_model_release_get()

    @property
    def vehicles_part_types_available(self):
        if not len(self._vehicles_part_types_available):
            self.vehicles_part_types_available_get()
        return self._vehicles_part_types_available

    @property
    def model_release_parts(self):
        if not len(self._model_release_parts):
            self.model_release_parts_get()
        return self._model_release_parts

    @property
    def vehicle_parts(self):
        if not len(self._vehicle_parts):
            self.vehicle_parts_get()
        return self._vehicle_parts

    @property
    def MODEL_RELEASE_ID(self):
        if self._MODEL_RELEASE_ID is None:
            self.vehicle_model_release_get()
        return self._MODEL_RELEASE_ID

    @arcimoto.db.transaction
    def vehicle_part_install(self, vin, part_type, part_number=None):
        vehicle = arcimoto.vehicle.Vehicle(vin)

        if not vehicle.exists:
            raise ArcimotoNotFoundError(f'Invalid vin: {vin}')
        self._VIN = vin

        if not self.part_type_exists(part_type):
            raise ArcimotoNotFoundError(f'Invalid part_type: {part_type}')

        if part_number is None:
            part_number = self.model_release_parts.get(part_type, None)
            if part_number is None:
                raise ArcimotoException(f'Invalid lookup of part_number from part_type {part_type}: {e}')

        if part_number is not None:
            if not self.part_number_exists_for_part_type_in_model_release(part_type, part_number):
                raise ArcimotoException(f'Invalid attempted parts configuration for model_release {self.MODEL_RELEASE_ID}')

        query = (
            'INSERT INTO vehicle_parts_installed '
            '(vin, part_type, part_number)'
            'VALUES (%s, %s, %s) '
            'ON CONFLICT ON CONSTRAINT vehicle_parts_installed_pkey DO UPDATE '
            'SET installed = NOW(), '
            'part_number = excluded.part_number '
            'RETURNING installed'
        )
        cursor = arcimoto.db.get_cursor()
        installed = None
        try:
            cursor.execute(query, [vin, part_type, part_number])
            result = cursor.fetchone()
            installed = result.get('installed', None)
        except Exception as e:
            raise ArcimotoException(f'Failure to insert {part_type}:{part_number} for {vin}: {e}')
        try:
            msg_part = 'Part Installed:\n{} - part_type: {}'.format(part_type, part_number)
            arcimoto.note.VehicleNote(
                vin=vin,
                message=msg_part,
                tags=['parts']
            )
        except Exception as e:
            raise ArcimotoException(f'Failure to create vehicle note for {vin}:{part_type}:{part_number} - {e}')

        return {
            'installed': arcimoto.db.datetime_record_output(installed) if installed else None,
            'part_type': part_type,
            'part_number': part_number
        }

    def vehicles_part_types_available_get(self):
        query = (
            'SELECT part_type '
            'FROM vehicle_part_types'
        )
        cursor = arcimoto.db.get_cursor()
        try:
            cursor.execute(query)
            for record in cursor.fetchall():
                self._vehicles_part_types_available.append(record['part_type'])
        except Exception as e:
            raise ArcimotoException(f'Failure to lookup part_types: {e}')

        return self._vehicles_part_types_available

    def model_release_parts_get(self):
        cursor = arcimoto.db.get_cursor()
        query = (
            'SELECT part_type, part_number '
            'FROM vehicle_model_parts '
            'WHERE model_release_id = %s'
        )
        try:
            cursor.execute(query, [self.MODEL_RELEASE_ID])
            self._model_release_parts = {}
            for record in cursor.fetchall():
                self._model_release_parts[record['part_type']] = record['part_number']
        except Exception as e:
            raise ArcimotoException(f'Failure to lookup map of firmware_components to part_types: {e}')

        return self._vehicle_parts

    def vehicle_parts_get(self):
        if not self._VIN:
            raise ArcimotoException(f'VIN not available, unable to fetch installed parts')
        cursor = arcimoto.db.get_cursor()
        query = (
            'SELECT part_type, part_number '
            'FROM vehicle_parts_installed '
            'WHERE vin = %s'
        )
        try:
            cursor.execute(query, [self._VIN])
            self._vehicle_parts = {}
            for record in cursor.fetchall():
                self._vehicle_parts[record['part_type']] = record['part_number']
        except Exception as e:
            raise ArcimotoException(f'Failure to lookup map of firmware_components to part_types: {e}')

        return self._vehicle_parts

    def part_type_exists(self, part_type):
        query = (
            'SELECT part_type FROM vehicle_part_types '
            'WHERE part_type = %s'
        )
        cursor = arcimoto.db.get_cursor()
        cursor.execute(query, [part_type])
        return cursor.rowcount >= 1

    def part_exists_for_model_release(self, part_number):
        query = (
            'SELECT part_number FROM vehicle_model_parts '
            'WHERE model_release_id = %s '
            'AND part_number = %s'
        )
        cursor = arcimoto.db.get_cursor()
        cursor.execute(query, [self.MODEL_RELEASE_ID, part_number])
        return cursor.rowcount >= 1

    def part_number_exists_for_part_type_in_model_release(self, part_type, part_number):
        query = (
            'SELECT part_number FROM vehicle_model_parts '
            'WHERE model_release_id = %s '
            'AND part_type = %s '
            'AND part_number = %s'
        )
        cursor = arcimoto.db.get_cursor()
        cursor.execute(query, [self.MODEL_RELEASE_ID, part_type, part_number])
        return cursor.rowcount >= 1

    @arcimoto.db.transaction
    def model_release_part_set(self, part_type, part_number):
        if not self.part_type_exists(part_type):
            raise ArcimotoNotFoundError(f'Invalid part_type: {part_type}')

        query = (
            'INSERT INTO vehicle_model_parts '
            '(model_release_id, part_type, part_number)'
            'VALUES (%s, %s, %s) '
            'ON CONFLICT ON CONSTRAINT vehicle_model_parts_model_release_id_part_type_ukey DO UPDATE '
            'SET created = NOW(), '
            'part_number = excluded.part_number '
            'RETURNING created'
        )
        cursor = arcimoto.db.get_cursor()
        created = None
        try:
            cursor.execute(query, [self.MODEL_RELEASE_ID, part_type, part_number])
            result = cursor.fetchone()
            created = result.get('created', None)
        except Exception as e:
            raise ArcimotoException(e)

        return {
            'created': arcimoto.db.datetime_record_output(created) if created else None,
            'part_type': part_type,
            'part_number': part_number
        }

    def vehicle_model_release_get(self):
        cursor = arcimoto.db.get_cursor()
        query = (
            'SELECT model_release_id FROM vehicle '
            'WHERE vin = %s'
        )
        cursor.execute(query, [self._VIN])
        result = cursor.fetchone()
        self._MODEL_RELEASE_ID = result.get('model_release_id')
