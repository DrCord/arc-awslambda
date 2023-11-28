import logging

from arcimoto.exceptions import *
import arcimoto.runtime
import arcimoto.user
import arcimoto.db

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


@arcimoto.runtime.handler
def locations_locations_list():
    global logger

    cursor = arcimoto.db.get_cursor()

    try:
        query = (
            'SELECT '
            'locations.id as id, '
            'location_name, '
            'lc.code as location_code, '
            'street_number, '
            'structure_name, '
            'street_number_suffix, '
            'street_name, '
            'street_type, '
            'street_direction, '
            'locations_address_types.address_type as address_type, '
            'address_type_identifier, '
            'city, '
            'governing_district, '
            'postal_area, '
            'local_municipality, '
            'country, '
            'gps_latitude, '
            'gps_longitude '
            'FROM locations '
            'LEFT JOIN locations_address_types '
            'ON locations.address_type = locations_address_types.id '
            'LEFT JOIN location_join_accounting_location_code AS jc '
            'ON locations.id = jc.location_id '
            'LEFT JOIN accounting_location_code AS lc '
            'ON lc.id = jc.accounting_location_code_id '
            'ORDER BY locations.id ASC'
        )
        cursor.execute(query)

        locations = []
        for record in cursor:
            locations.append(
                {
                    'id': record['id'],
                    'location_name': record['location_name'],
                    'location_code': record['location_code'],
                    'street_number': record['street_number'],
                    'structure_name': record['structure_name'],
                    'street_number_suffix': record['street_number_suffix'],
                    'street_name': record['street_name'],
                    'street_type': record['street_type'],
                    'street_direction': record['street_direction'],
                    'address_type': record['address_type'],
                    'address_type_identifier': record['address_type_identifier'],
                    'city': record['city'],
                    'governing_district': record['governing_district'],
                    'postal_area': record['postal_area'],
                    'local_municipality': record['local_municipality'],
                    'country': record['country'],
                    'gps_latitude': record['gps_latitude'],
                    'gps_longitude': record['gps_longitude']
                }
            )
    except Exception as e:
        raise ArcimotoException(f'Unable to get locations: {e}') from e

    return {'locations': locations}


lambda_handler = locations_locations_list
