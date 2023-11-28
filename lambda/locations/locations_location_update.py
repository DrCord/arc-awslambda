import logging

from arcimoto.exceptions import *
import arcimoto.runtime
import arcimoto.user
import arcimoto.db
import arcimoto.args

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

arcimoto.args.register({
    'id': {
        'type': 'integer',
        'required': True,
        'min': 1
    },
    'location_name': {
        'type': 'string',
        'required': True,
        'empty': False
    },
    'street_number': {
        'type': 'integer',
        'min': 1,
        'nullable': True
    },
    'structure_name': {
        'type': 'string',
        'empty': False,
        'nullable': True
    },
    'street_number_suffix': {
        'type': 'string',
        'empty': False,
        'nullable': True
    },
    'street_name': {
        'type': 'string',
        'empty': False,
        'nullable': True
    },
    'street_type': {
        'type': 'string',
        'empty': False,
        'nullable': True
    },
    'street_direction': {
        'type': 'string',
        'empty': False,
        'nullable': True
    },
    'address_type': {
        'type': 'integer',
        'min': 1,
        'nullable': True
    },
    'address_type_identifier': {
        'type': 'string',
        'empty': False,
        'nullable': True
    },
    'city': {
        'type': 'string',
        'empty': False,
        'nullable': True
    },
    'governing_district': {
        'type': 'string',
        'empty': False,
        'nullable': True
    },
    'postal_area': {
        'type': 'string',
        'empty': False,
        'nullable': True
    },
    'local_municipality': {
        'type': 'string',
        'empty': False,
        'nullable': True
    },
    'country': {
        'type': 'string',
        'empty': False,
        'allowed': [
            'AI',
            'AQ',
            'AG',
            'AR',
            'AM',
            'AW',
            'AU',
            'AT',
            'AZ',
            'BH',
            'BS',
            'BD',
            'BB',
            'BY',
            'BE',
            'BZ',
            'BJ',
            'BM',
            'BT',
            'BO',
            'BQ',
            'BA',
            'BW',
            'BV',
            'BR',
            'IO',
            'BN',
            'BG',
            'BF',
            'BI',
            'KH',
            'CM',
            'CA',
            'CV',
            'KY',
            'CF',
            'TD',
            'CL',
            'CN',
            'CX',
            'CC',
            'CO',
            'KM',
            'CG',
            'CD',
            'CK',
            'CR',
            'CI',
            'HR',
            'CU',
            'CW',
            'CY',
            'CZ',
            'DK',
            'DJ',
            'DM',
            'DO',
            'EC',
            'EG',
            'SV',
            'GQ',
            'ER',
            'EE',
            'ET',
            'FK',
            'FO',
            'FJ',
            'FI',
            'FR',
            'GF',
            'PF',
            'TF',
            'GA',
            'GM',
            'GE',
            'DE',
            'GH',
            'GI',
            'GR',
            'GL',
            'GD',
            'GP',
            'GU',
            'GT',
            'GG',
            'GN',
            'GW',
            'GY',
            'HT',
            'HM',
            'VA',
            'HN',
            'HK',
            'HU',
            'IS',
            'IN',
            'ID',
            'IR',
            'IQ',
            'IE',
            'IM',
            'IL',
            'IT',
            'JM',
            'JP',
            'JE',
            'JO',
            'KZ',
            'KE',
            'KI',
            'KP',
            'KR',
            'KW',
            'KG',
            'LA',
            'LV',
            'LB',
            'LS',
            'LR',
            'LY',
            'LI',
            'LT',
            'LU',
            'MO',
            'MK',
            'MG',
            'MW',
            'MY',
            'MV',
            'ML',
            'MT',
            'MH',
            'MQ',
            'MR',
            'MU',
            'YT',
            'MX',
            'FM',
            'MD',
            'MC',
            'MN',
            'ME',
            'MS',
            'MA',
            'MZ',
            'MM',
            'NA',
            'NR',
            'NP',
            'NL',
            'NC',
            'NZ',
            'NI',
            'NE',
            'NG',
            'NU',
            'NF',
            'MP',
            'NO',
            'OM',
            'PK',
            'PW',
            'PS',
            'PA',
            'PG',
            'PY',
            'PE',
            'PH',
            'PN',
            'PL',
            'PT',
            'PR',
            'QA',
            'RE',
            'RO',
            'RU',
            'RW',
            'BL',
            'SH',
            'KN',
            'LC',
            'MF',
            'PM',
            'VC',
            'WS',
            'SM',
            'ST',
            'SA',
            'SN',
            'RS',
            'SC',
            'SL',
            'SG',
            'SX',
            'SK',
            'SI',
            'SB',
            'SO',
            'ZA',
            'GS',
            'SS',
            'ES',
            'LK',
            'SD',
            'SR',
            'SJ',
            'SZ',
            'SE',
            'CH',
            'SY',
            'TW',
            'TJ',
            'TZ',
            'TH',
            'TL',
            'TG',
            'TK',
            'TO',
            'TT',
            'TN',
            'TR',
            'TM',
            'TC',
            'TV',
            'UG',
            'UA',
            'AE',
            'GB',
            'US',
            'UM',
            'UY',
            'UZ',
            'VU',
            'VE',
            'VN',
            'VG',
            'VI',
            'WF',
            'EH',
            'YE',
            'ZM',
            'ZW'
        ],
        'nullable': True
    },
    'gps_latitude': {
        'type': 'float',
        'nullable': True
    },
    'gps_longitude': {
        'type': 'float',
        'nullable': True
    },
})


@arcimoto.runtime.handler
@arcimoto.user.require('locations.update')
@arcimoto.db.transaction
def locations_location_update(
    id,
    location_name,
    street_number,
    structure_name,
    street_number_suffix,
    street_name,
    street_type,
    street_direction,
    address_type,
    address_type_identifier,
    city,
    governing_district,
    postal_area,
    local_municipality,
    country,
    gps_latitude,
    gps_longitude
):
    global logger

    def address_type_get(id):
        for item in address_types:
            if item.get('id') == id:
                return item.get('address_type')
        return

    cursor = arcimoto.db.get_cursor()

    try:
        query = (
            'SELECT '
            'id, address_type '
            'FROM locations_address_types'
        )
        cursor.execute(query)
        address_types = []
        for record in cursor:
            address_types.append(
                {
                    'id': record['id'],
                    'address_type': record['address_type']
                }
            )
    except Exception as e:
        raise ArcimotoException(f'Unable to get address types: {e}') from e

    try:
        if (    not location_name
            and not street_number
            and not structure_name
            and not street_number_suffix
            and not street_name
            and not street_type
            and not street_direction
            and not address_type
            and not address_type_identifier
            and not city
            and not governing_district
            and not postal_area
            and not local_municipality
            and not country
            and not gps_latitude
            and not gps_longitude
        ):
            raise ArcimotoArgumentError('You must supply a field to edit the record')

        where_predicates = [
            {
                'column': 'id',
                'operator': '=',
                'value': id
            }
        ]
        columns_data = [
            {'location_name': location_name},
            {'street_number': street_number},
            {'structure_name': structure_name},
            {'street_number_suffix': street_number_suffix},
            {'street_name': street_name},
            {'street_type': street_type},
            {'street_direction': street_direction},
            {'address_type': address_type},
            {'address_type_identifier': address_type_identifier},
            {'city': city},
            {'governing_district': governing_district},
            {'postal_area': postal_area},
            {'local_municipality': local_municipality},
            {'country': country},
            {'gps_latitude': gps_latitude},
            {'gps_longitude': gps_longitude}
        ]
        cursor.execute(
            *arcimoto.db.prepare_update_query_and_params(
                'locations',
                where_predicates,
                columns_data,
                True
            )
        )
        record = cursor.fetchone()

        output = {
                'id': record['id'],
                'location_name': record['location_name'],
                'street_number': record['street_number'],
                'structure_name': record['structure_name'],
                'street_number_suffix': record['street_number_suffix'],
                'street_name': record['street_name'],
                'street_type': record['street_type'],
                'street_direction': record['street_direction'],
                'address_type': address_type_get(record['address_type']) if record['address_type'] is not None else None,
                'address_type_identifier': record['address_type_identifier'],
                'city': record['city'],
                'governing_district': record['governing_district'],
                'postal_area': record['postal_area'],
                'local_municipality': record['local_municipality'],
                'country': record['country'],
                'gps_latitude': record['gps_latitude'],
                'gps_longitude': record['gps_longitude']
            }
    except Exception as e:
        raise ArcimotoException(f'Unable to update location record with id {id}: {e}') from e

    return output


lambda_handler = locations_location_update
