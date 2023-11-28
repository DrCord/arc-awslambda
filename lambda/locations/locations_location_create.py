import logging

from arcimoto.exceptions import *
import arcimoto.runtime
import arcimoto.db

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

arcimoto.args.register({
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
@arcimoto.db.transaction
def locations_location_create(
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

    cursor = arcimoto.db.get_cursor()
    current_user = arcimoto.user.current()

    query = (
        'INSERT INTO '
        'locations '
        '('
        'location_name, '
        'street_number, '
        'structure_name, '
        'street_number_suffix, '
        'street_name, '
        'street_type, '
        'street_direction, '
        'address_type, '
        'address_type_identifier, '
        'city, '
        'governing_district, '
        'postal_area, '
        'local_municipality, '
        'country, '
        'gps_latitude, '
        'gps_longitude, '
        'created_by'
        ') '
        'VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) '
        'RETURNING id'
    )
    try:
        cursor.execute(query, [
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
            gps_longitude,
            current_user.username
        ])
        result_set = cursor.fetchone()
        id = result_set['id'] if result_set is not None else None
    except Exception as e:
        raise ArcimotoException(f'Unable to create location: {e}') from e

    return {'id': id}


lambda_handler = locations_location_create
