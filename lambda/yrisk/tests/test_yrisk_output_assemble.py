import logging
import unittest
import copy

from arcimoto.exceptions import *
import arcimoto.runtime
import arcimoto.tests
import yrisk_functions

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class YriskOutputAssembleTestCase(unittest.TestCase):

    vehicles_db_data = {
        'vehicles': [
        {
            'vin': 'DEV-7F7ADR310MER00013',
            'location': {
                'name': 'Arcimoto World Headquarters',
                'city': 'Eugene',
                'state': 'Oregon'
            },
            'coverage': 'pilot',
            'model': 'Deliverator'
        },
        {
            'vin': 'DEV-7F7ADR311LER00004',
            'location': {
                'name': 'Arcimoto World Headquarters',
                'city': 'Eugene',
                'state': 'Oregon'
            },
            'coverage': 'pilot',
            'model': 'Deliverator'
        },
        {
            'vin': 'DEV-7F7ADR311MER00005',
            'location': {
                'name': 'Arcimoto World Headquarters',
                'city': 'Eugene',
                'state': 'Oregon'
            },
            'coverage': 'pilot',
            'model': 'Deliverator'
        },
        {
            'vin': 'DEV-7F7ADR311MER00019',
            'location': {
                'name': 'Arcimoto World Headquarters',
                'city': 'Eugene',
                'state': 'Oregon'
            },
            'coverage': 'pilot',
            'model': 'Deliverator'
        },
        {
            'vin': 'DEV-7F7ADR311MER00022',
            'location': {
                'name': 'Arcimoto World Headquarters',
                'city': 'Eugene',
                'state': 'Oregon'
            },
            'coverage': 'pilot',
            'model': 'Deliverator'
        },
        {
            'vin': 'DEV-7F7ADR312MER00014',
            'location': {
                'name': 'Arcimoto World Headquarters',
                'city': 'Eugene',
                'state': 'Oregon'
            },
            'coverage': 'pilot',
            'model': 'Deliverator'
        },
        {
            'vin': 'DEV-7F7ADR313LER00005',
            'location': {
                'name': 'Arcimoto World Headquarters',
                'city': 'Eugene',
                'state': 'Oregon'
            },
            'coverage': 'pilot',
            'model': 'Deliverator'
        },
        {
            'vin': 'DEV-7F7ADR313MER00006',
            'location': {
                'name': 'Arcimoto World Headquarters',
                'city': 'Eugene',
                'state': 'Oregon'
            },
            'coverage': 'pilot',
            'model': 'Deliverator'
        },
        {
            'vin': 'DEV-7F7ADR314MER00001',
            'location': {
                'name': 'Arcimoto World Headquarters',
                'city': 'Eugene',
                'state': 'Oregon'
            },
            'coverage': 'internal',
            'model': 'Deliverator'
        },
        {
            'vin': 'DEV-7F7ADR314MER00015',
            'location': {
                'name': 'Arcimoto World Headquarters',
                'city': 'Eugene',
                'state': 'Oregon'
            },
            'coverage': 'pilot',
            'model': 'Deliverator'
        },
        {
            'vin': 'DEV-7F7ADR315LER00006',
            'location': {
                'name': 'Arcimoto World Headquarters',
                'city': 'Eugene',
                'state': 'Oregon'
            },
            'coverage': 'pilot',
            'model': 'Deliverator'
        },
        {
            'vin': 'DEV-7F7ADR315MER00007',
            'location': {
                'name': 'Arcimoto World Headquarters',
                'city': 'Eugene',
                'state': 'Oregon'
            },
            'coverage': 'pilot',
            'model': 'Deliverator'
        },
        {
            'vin': 'DEV-7F7ADR315MER00010',
            'location': {
                'name': 'Arcimoto World Headquarters',
                'city': 'Eugene',
                'state': 'Oregon'
            },
            'coverage': 'pilot',
            'model': 'Deliverator'
        },
        {
            'vin': 'DEV-7F7ADR316LER00001',
            'location': {
                'name': 'Arcimoto World Headquarters',
                'city': 'Eugene',
                'state': 'Oregon'
            },
            'coverage': 'pilot',
            'model': 'Deliverator'
        },
        {
            'vin': 'DEV-7F7ADR316MER00016',
            'location': {
                'name': 'Arcimoto World Headquarters',
                'city': 'Eugene',
                'state': 'Oregon'
            },
            'coverage': 'pilot',
            'model': 'Deliverator'
        },
        {
            'vin': 'DEV-7F7ADR317MER00008',
            'location': {
                'name': 'Arcimoto World Headquarters',
                'city': 'Eugene',
                'state': 'Oregon'
            },
            'coverage': 'pilot',
            'model': 'Deliverator'
        },
        {
            'vin': 'DEV-7F7ADR317MER00011',
            'location': {
                'name': 'Arcimoto World Headquarters',
                'city': 'Eugene',
                'state': 'Oregon'
            },
            'coverage': 'internal',
            'model': 'Deliverator'
        },
        {
            'vin': 'DEV-7F7ADR318LER00002',
            'location': {
                'name': 'Arcimoto World Headquarters',
                'city': 'Eugene',
                'state': 'Oregon'
            },
            'coverage': 'pilot',
            'model': 'Deliverator'
        },
        {
            'vin': 'DEV-7F7ADR318MER00017',
            'location': {
                'name': 'Arcimoto World Headquarters',
                'city': 'Eugene',
                'state': 'Oregon'
            },
            'coverage': 'pilot',
            'model': 'Deliverator'
        },
        {
            'vin': 'DEV-7F7ADR318MER00020',
            'location': {
                'name': 'Arcimoto World Headquarters',
                'city': 'Eugene',
                'state': 'Oregon'
            },
            'coverage': 'internal',
            'model': 'Deliverator'
        },
        {
            'vin': 'DEV-7F7ADR319MER00009',
            'location': {
                'name': 'Arcimoto World Headquarters',
                'city': 'Eugene',
                'state': 'Oregon'
            },
            'coverage': 'pilot',
            'model': 'Deliverator'
        },
        {
            'vin': 'DEV-7F7ADR319MER00012',
            'location': {
                'name': 'Arcimoto World Headquarters',
                'city': 'Eugene',
                'state': 'Oregon'
            },
            'coverage': 'pilot',
            'model': 'Deliverator'
        },
        {
            'vin': 'DEV-7F7ADR31XLER00003',
            'location': {
                'name': 'Arcimoto World Headquarters',
                'city': 'Eugene',
                'state': 'Oregon'
            },
            'coverage': 'pilot',
            'model': 'Deliverator'
        },
        {
            'vin': 'DEV-7F7ADR31XMER00004',
            'location': {
                'name': 'Arcimoto World Headquarters',
                'city': 'Eugene',
                'state': 'Oregon'
            },
            'coverage': 'pilot',
            'model': 'Deliverator'
        },
        {
            'vin': 'DEV-7F7ADR31XMER00018',
            'location': {
                'name': 'Arcimoto World Headquarters',
                'city': 'Eugene',
                'state': 'Oregon'
            },
            'coverage': 'pilot',
            'model': 'Deliverator'
        },
        {
            'vin': 'DEV-7F7ADR31XMER00021',
            'location': {
                'name': 'Arcimoto World Headquarters',
                'city': 'Eugene',
                'state': 'Oregon'
            },
            'coverage': 'internal',
            'model': 'Deliverator'
        },
        {
            'vin': 'DEV-7F7AER318MER00001',
            'location': {
                'name': 'Arcimoto World Headquarters',
                'city': 'Eugene',
                'state': 'Oregon'
            },
            'coverage': 'internal',
            'model': 'Rapid Responder'
        },
        {
            'vin': 'DEV-7F7ARR311MER00006',
            'location': {
                'name': 'Arcimoto World Headquarters',
                'city': 'Eugene',
                'state': 'Oregon'
            },
            'coverage': 'internal',
            'model': 'Roadster'
        },
        {
            'vin': 'DEV-7F7ARR312MER00001',
            'location': {
                'name': 'Arcimoto World Headquarters',
                'city': 'Eugene',
                'state': 'Oregon'
            },
            'coverage': 'internal',
            'model': 'Roadster'
        },
        {
            'vin': 'DEV-7F7ARR313MER00007',
            'location': {
                'name': 'Arcimoto World Headquarters',
                'city': 'Eugene',
                'state': 'Oregon'
            },
            'coverage': 'internal',
            'model': 'Roadster'
        },
        {
            'vin': 'DEV-7F7ARR314LER00001',
            'location': {
                'name': 'Arcimoto World Headquarters',
                'city': 'Eugene',
                'state': 'Oregon'
            },
            'coverage': 'internal',
            'model': 'Roadster'
        },
        {
            'vin': 'DEV-7F7ARR314MER00002',
            'location': {
                'name': 'Arcimoto World Headquarters',
                'city': 'Eugene',
                'state': 'Oregon'
            },
            'coverage': 'internal',
            'model': 'Roadster'
        },
        {
            'vin': 'DEV-7F7ARR316LER00002',
            'location': {
                'name': 'Arcimoto World Headquarters',
                'city': 'Eugene',
                'state': 'Oregon'
            },
            'coverage': 'internal',
            'model': 'Roadster'
        },
        {
            'vin': 'DEV-7F7ARR316MER00003',
            'location': {
                'name': 'Arcimoto World Headquarters',
                'city': 'Eugene',
                'state': 'Oregon'
            },
            'coverage': 'internal',
            'model': 'Roadster'
        },
        {
            'vin': 'DEV-7F7ARR318LER00003',
            'location': {
                'name': 'Arcimoto World Headquarters',
                'city': 'Eugene',
                'state': 'Oregon'
            },
            'coverage': 'internal',
            'model': 'Roadster'
        },
        {
            'vin': 'DEV-7F7ARR318MER00004',
            'location': {
                'name': 'Arcimoto World Headquarters',
                'city': 'Eugene',
                'state': 'Oregon'
            },
            'coverage': 'internal',
            'model': 'Roadster'
        },
        {
            'vin': 'DEV-7F7ARR31XLER00004',
            'location': {
                'name': 'Arcimoto World Headquarters',
                'city': 'Eugene',
                'state': 'Oregon'
            },
            'coverage': 'internal',
            'model': 'Roadster'
        },
        {
            'vin': 'DEV-7F7ARR31XMER00005',
            'location': {
                'name': 'Arcimoto World Headquarters',
                'city': 'Eugene',
                'state': 'Oregon'
            },
            'coverage': 'internal',
            'model': 'Roadster'
        },
        {
            'vin': 'DEV-7F7ATR310MER00029',
            'location': {
                'name': 'Arcimoto Rental Facility [San Diego]',
                'city': 'San Diego',
                'state': 'California'
            },
            'coverage': 'rental',
            'model': 'FUV'
        },
        {
            'vin': 'DEV-7F7ATR310MER00077',
            'location': {
                'name': 'Arcimoto Rental Facility [Eugene]',
                'city': 'Eugene',
                'state': 'Oregon'
            },
            'coverage': 'rental',
            'model': 'FUV'
        },
        {
            'vin': 'DEV-7F7ATR310MER00080',
            'location': {
                'name': 'Arcimoto World Headquarters',
                'city': 'Eugene',
                'state': 'Oregon'
            },
            'coverage': 'internal',
            'model': 'FUV'
        },
        {
            'vin': 'DEV-7F7ATR310MER00130',
            'location': {
                'name': 'Arcimoto Rental Facility [San Diego]',
                'city': 'San Diego',
                'state': 'California'
            },
            'coverage': 'rental',
            'model': 'FUV'
        },
        {
            'vin': 'DEV-7F7ATR311LER00023',
            'location': {
                'name': 'Arcimoto World Headquarters',
                'city': 'Eugene',
                'state': 'Oregon'
            },
            'coverage': 'internal',
            'model': 'FUV'
        },
        {
            'vin': 'DEV-7F7ATR311LER00085',
            'location': {
                'name': 'Arcimoto World Headquarters',
                'city': 'Eugene',
                'state': 'Oregon'
            },
            'coverage': 'internal',
            'model': 'FUV'
        },
        {
            'vin': 'DEV-7F7ATR311MER00055',
            'location': {
                'name': 'Arcimoto World Headquarters',
                'city': 'Eugene',
                'state': 'Oregon'
            },
            'coverage': 'internal',
            'model': 'FUV'
        },
        {
            'vin': 'DEV-7F7ATR311MER00072',
            'location': {
                'name': 'Arcimoto World Headquarters',
                'city': 'Eugene',
                'state': 'Oregon'
            },
            'coverage': 'pilot',
            'model': 'FUV'
        },
        {
            'vin': 'DEV-7F7ATR311MER00086',
            'location': {
                'name': 'Arcimoto Rental Facility [Eugene]',
                'city': 'Eugene',
                'state': 'Oregon'
            },
            'coverage': 'rental',
            'model': 'FUV'
        },
        {
            'vin': 'DEV-7F7ATR311MER00122',
            'location': {
                'name': 'Arcimoto World Headquarters',
                'city': 'Eugene',
                'state': 'Oregon'
            },
            'coverage': 'internal',
            'model': 'FUV'
        },
        {
            'vin': 'DEV-7F7ATR311MER00136',
            'location': {
                'name': 'Arcimoto Rental Facility [Eugene]',
                'city': 'Eugene',
                'state': 'Oregon'
            },
            'coverage': 'rental',
            'model': 'FUV'
        },
        {
            'vin': 'DEV-7F7ATR312LER00015',
            'location': {
                'name': 'Arcimoto World Headquarters',
                'city': 'Eugene',
                'state': 'Oregon'
            },
            'coverage': 'internal',
            'model': 'FUV'
        },
        {
            'vin': 'DEV-7F7ATR312LER00046',
            'location': {
                'name': 'Arcimoto World Headquarters',
                'city': 'Eugene',
                'state': 'Oregon'
            },
            'coverage': 'pilot',
            'model': 'FUV'
        },
        {
            'vin': 'DEV-7F7ATR312MER00131',
            'location': {
                'name': 'Arcimoto Rental Facility [San Diego]',
                'city': 'San Diego',
                'state': 'California'
            },
            'coverage': 'rental',
            'model': 'FUV'
        },
        {
            'vin': 'DEV-7F7ATR312MER00159',
            'location': {
                'name': 'Arcimoto Rental Facility [Eugene]',
                'city': 'Eugene',
                'state': 'Oregon'
            },
            'coverage': 'rental',
            'model': 'FUV'
        },
        {
            'vin': 'DEV-7F7ATR313LER00010',
            'location': {
                'name': 'Arcimoto World Headquarters',
                'city': 'Eugene',
                'state': 'Oregon'
            },
            'coverage': 'internal',
            'model': 'FUV'
        },
        {
            'vin': 'DEV-7F7ATR313LER00038',
            'location': {
                'name': 'Arcimoto World Headquarters',
                'city': 'Eugene',
                'state': 'Oregon'
            },
            'coverage': 'internal',
            'model': 'FUV'
        },
        {
            'vin': 'DEV-7F7ATR313LER00086',
            'location': {
                'name': 'Arcimoto World Headquarters',
                'city': 'Eugene',
                'state': 'Oregon'
            },
            'coverage': 'internal',
            'model': 'FUV'
        },
        {
            'vin': 'DEV-7F7ATR313MER00073',
            'location': {
                'name': 'Arcimoto Rental Facility [Eugene]',
                'city': 'Eugene',
                'state': 'Oregon'
            },
            'coverage': 'rental',
            'model': 'FUV'
        },
        {
            'vin': 'DEV-7F7ATR313MER00087',
            'location': {
                'name': 'Arcimoto Rental Facility [Eugene]',
                'city': 'Eugene',
                'state': 'Oregon'
            },
            'coverage': 'rental',
            'model': 'FUV'
        },
        {
            'vin': 'DEV-7F7ATR313MER00090',
            'location': {
                'name': 'Arcimoto Rental Facility [Eugene]',
                'city': 'Eugene',
                'state': 'Oregon'
            },
            'coverage': 'rental',
            'model': 'FUV'
        },
        {
            'vin': 'DEV-7F7ATR313MER00137',
            'location': {
                'name': 'Arcimoto World Headquarters',
                'city': 'Eugene',
                'state': 'Oregon'
            },
            'coverage': 'pilot',
            'model': 'FUV'
        },
        {
            'vin': 'DEV-7F7ATR313MER00154',
            'location': {
                'name': 'Arcimoto Rental Facility [Eugene]',
                'city': 'Eugene',
                'state': 'Oregon'
            },
            'coverage': 'rental',
            'model': 'FUV'
        },
        {
            'vin': 'DEV-7F7ATR314KER00015',
            'location': {
                'name': 'Arcimoto World Headquarters',
                'city': 'Eugene',
                'state': 'Oregon'
            },
            'coverage': 'pilot',
            'model': 'FUV'
        },
        {
            'vin': 'DEV-7F7ATR314KER00032',
            'location': {
                'name': 'Arcimoto World Headquarters',
                'city': 'Eugene',
                'state': 'Oregon'
            },
            'coverage': 'internal',
            'model': 'FUV'
        },
        {
            'vin': 'DEV-7F7ATR314LER00047',
            'location': {
                'name': 'Arcimoto World Headquarters',
                'city': 'Eugene',
                'state': 'Oregon'
            },
            'coverage': 'pilot',
            'model': 'FUV'
        },
        {
            'vin': 'DEV-7F7ATR314LER00081',
            'location': {
                'name': 'Arcimoto World Headquarters',
                'city': 'Eugene',
                'state': 'Oregon'
            },
            'coverage': 'internal',
            'model': 'FUV'
        },
        {
            'vin': 'DEV-7F7ATR314MER00082',
            'location': {
                'name': 'Arcimoto World Headquarters',
                'city': 'Eugene',
                'state': 'Oregon'
            },
            'coverage': 'pilot',
            'model': 'FUV'
        },
        {
            'vin': 'DEV-7F7ATR314MER00129',
            'location': {
                'name': 'Arcimoto Rental Facility [San Diego]',
                'city': 'San Diego',
                'state': 'California'
            },
            'coverage': 'rental',
            'model': 'FUV'
        },
        {
            'vin': 'DEV-7F7ATR314MER00132',
            'location': {
                'name': 'Arcimoto Rental Facility [San Diego]',
                'city': 'San Diego',
                'state': 'California'
            },
            'coverage': 'rental',
            'model': 'FUV'
        },
        {
            'vin': 'DEV-7F7ATR314MER00163',
            'location': {
                'name': 'Arcimoto World Headquarters',
                'city': 'Eugene',
                'state': 'Oregon'
            },
            'coverage': 'internal',
            'model': 'FUV'
        },
        {
            'vin': 'DEV-7F7ATR315LER00011',
            'location': {
                'name': 'Arcimoto World Headquarters',
                'city': 'Eugene',
                'state': 'Oregon'
            },
            'coverage': 'internal',
            'model': 'FUV'
        },
        {
            'vin': 'DEV-7F7ATR315LER00042',
            'location': {
                'name': 'Arcimoto World Headquarters',
                'city': 'Eugene',
                'state': 'Oregon'
            },
            'coverage': 'internal',
            'model': 'FUV'
        },
        {
            'vin': 'DEV-7F7ATR315LER00087',
            'location': {
                'name': 'Arcimoto World Headquarters',
                'city': 'Eugene',
                'state': 'Oregon'
            },
            'coverage': 'internal',
            'model': 'FUV'
        },
        {
            'vin': 'DEV-7F7ATR315MER00074',
            'location': {
                'name': 'Arcimoto Rental Facility [Eugene]',
                'city': 'Eugene',
                'state': 'Oregon'
            },
            'coverage': 'rental',
            'model': 'FUV'
        },
        {
            'vin': 'DEV-7F7ATR315MER00091',
            'location': {
                'name': 'Arcimoto Rental Facility [Eugene]',
                'city': 'Eugene',
                'state': 'Oregon'
            },
            'coverage': 'rental',
            'model': 'FUV'
        },
        {
            'vin': 'DEV-7F7ATR315MER00138',
            'location': {
                'name': 'Arcimoto World Headquarters',
                'city': 'Eugene',
                'state': 'Oregon'
            },
            'coverage': 'pilot',
            'model': 'FUV'
        },
        {
            'vin': 'DEV-7F7ATR315MER00155',
            'location': {
                'name': 'Arcimoto Rental Facility [Eugene]',
                'city': 'Eugene',
                'state': 'Oregon'
            },
            'coverage': 'rental',
            'model': 'FUV'
        },
        {
            'vin': 'DEV-7F7ATR316LER00082',
            'location': {
                'name': 'Arcimoto World Headquarters',
                'city': 'Eugene',
                'state': 'Oregon'
            },
            'coverage': 'internal',
            'model': 'FUV'
        },
        {
            'vin': 'DEV-7F7ATR316MER00097',
            'location': {
                'name': 'Arcimoto Rental Facility [Orlando]',
                'city': 'Orlando',
                'state': 'Florida'
            },
            'coverage': 'rental',
            'model': 'FUV'
        },
        {
            'vin': 'DEV-7F7ATR316MER00102',
            'location': {
                'name': 'Arcimoto World Headquarters',
                'city': 'Eugene',
                'state': 'Oregon'
            },
            'coverage': 'internal',
            'model': 'FUV'
        },
        {
            'vin': 'DEV-7F7ATR316MER00133',
            'location': {
                'name': 'Arcimoto Rental Facility [San Diego]',
                'city': 'San Diego',
                'state': 'California'
            },
            'coverage': 'rental',
            'model': 'FUV'
        },
        {
            'vin': 'DEV-7F7ATR316MER00164',
            'location': {
                'name': 'Arcimoto World Headquarters',
                'city': 'Eugene',
                'state': 'Oregon'
            },
            'coverage': 'pilot',
            'model': 'FUV'
        },
        {
            'vin': 'DEV-7F7ATR317LER00088',
            'location': {
                'name': 'Arcimoto World Headquarters',
                'city': 'Eugene',
                'state': 'Oregon'
            },
            'coverage': 'internal',
            'model': 'FUV'
        },
        {
            'vin': 'DEV-7F7ATR317MER00027',
            'location': {
                'name': 'Arcimoto Rental Facility [San Diego]',
                'city': 'San Diego',
                'state': 'California'
            },
            'coverage': 'rental',
            'model': 'FUV'
        },
        {
            'vin': 'DEV-7F7ATR317MER00030',
            'location': {
                'name': 'Arcimoto Rental Facility [San Diego]',
                'city': 'San Diego',
                'state': 'California'
            },
            'coverage': 'rental',
            'model': 'FUV'
        },
        {
            'vin': 'DEV-7F7ATR317MER00075',
            'location': {
                'name': 'Arcimoto Rental Facility [Eugene]',
                'city': 'Eugene',
                'state': 'Oregon'
            },
            'coverage': 'rental',
            'model': 'FUV'
        },
        {
            'vin': 'DEV-7F7ATR317MER00089',
            'location': {
                'name': 'Arcimoto Rental Facility [Eugene]',
                'city': 'Eugene',
                'state': 'Oregon'
            },
            'coverage': 'rental',
            'model': 'FUV'
        },
        {
            'vin': 'DEV-7F7ATR317MER00092',
            'location': {
                'name': 'Arcimoto Rental Facility [Eugene]',
                'city': 'Eugene',
                'state': 'Oregon'
            },
            'coverage': 'rental',
            'model': 'FUV'
        },
        {
            'vin': 'DEV-7F7ATR317MER00139',
            'location': {
                'name': 'Arcimoto World Headquarters',
                'city': 'Eugene',
                'state': 'Oregon'
            },
            'coverage': 'pilot',
            'model': 'FUV'
        },
        {
            'vin': 'DEV-7F7ATR317MER00156',
            'location': {
                'name': 'Arcimoto Rental Facility [Eugene]',
                'city': 'Eugene',
                'state': 'Oregon'
            },
            'coverage': 'rental',
            'model': 'FUV'
        },
        {
            'vin': 'DEV-7F7ATR318KER00003',
            'location': {
                'name': 'Arcimoto World Headquarters',
                'city': 'Eugene',
                'state': 'Oregon'
            },
            'coverage': 'internal',
            'model': 'FUV'
        },
        {
            'vin': 'DEV-7F7ATR318LER00052',
            'location': {
                'name': 'Arcimoto World Headquarters',
                'city': 'Eugene',
                'state': 'Oregon'
            },
            'coverage': 'pilot',
            'model': 'FUV'
        },
        {
            'vin': 'DEV-7F7ATR318LER00083',
            'location': {
                'name': 'Arcimoto World Headquarters',
                'city': 'Eugene',
                'state': 'Oregon'
            },
            'coverage': 'internal',
            'model': 'FUV'
        },
        {
            'vin': 'DEV-7F7ATR318MER00084',
            'location': {
                'name': 'Arcimoto World Headquarters',
                'city': 'Eugene',
                'state': 'Oregon'
            },
            'coverage': 'internal',
            'model': 'FUV'
        },
        {
            'vin': 'DEV-7F7ATR318MER00098',
            'location': {
                'name': 'Arcimoto Rental Facility [Orlando]',
                'city': 'Orlando',
                'state': 'Florida'
            },
            'coverage': 'rental',
            'model': 'FUV'
        },
        {
            'vin': 'DEV-7F7ATR318MER00134',
            'location': {
                'name': 'Arcimoto Rental Facility [Eugene]',
                'city': 'Eugene',
                'state': 'Oregon'
            },
            'coverage': 'rental',
            'model': 'FUV'
        },
        {
            'vin': 'DEV-7F7ATR319KER00009',
            'location': {
                'name': 'Arcimoto World Headquarters',
                'city': 'Eugene',
                'state': 'Oregon'
            },
            'coverage': 'internal',
            'model': 'FUV'
        },
        {
            'vin': 'DEV-7F7ATR319LER00044',
            'location': {
                'name': 'Arcimoto World Headquarters',
                'city': 'Eugene',
                'state': 'Oregon'
            },
            'coverage': 'pilot',
            'model': 'FUV'
        },
        {
            'vin': 'DEV-7F7ATR319MER00028',
            'location': {
                'name': 'Arcimoto Rental Facility [San Diego]',
                'city': 'San Diego',
                'state': 'California'
            },
            'coverage': 'rental',
            'model': 'FUV'
        },
        {
            'vin': 'DEV-7F7ATR319MER00031',
            'location': {
                'name': 'Arcimoto Rental Facility [Orlando]',
                'city': 'Orlando',
                'state': 'Florida'
            },
            'coverage': 'rental',
            'model': 'FUV'
        },
        {
            'vin': 'DEV-7F7ATR319MER00076',
            'location': {
                'name': 'Arcimoto Rental Facility [Eugene]',
                'city': 'Eugene',
                'state': 'Oregon'
            },
            'coverage': 'rental',
            'model': 'FUV'
        },
        {
            'vin': 'DEV-7F7ATR31XKER00004',
            'location': {
                'name': 'Arcimoto World Headquarters',
                'city': 'Eugene',
                'state': 'Oregon'
            },
            'coverage': 'internal',
            'model': 'FUV'
        },
        {
            'vin': 'DEV-7F7ATR31XLER00084',
            'location': {
                'name': 'Arcimoto World Headquarters',
                'city': 'Eugene',
                'state': 'Oregon'
            },
            'coverage': 'internal',
            'model': 'FUV'
        },
        {
            'vin': 'DEV-7F7ATR31XLER00117',
            'location': {
                'name': 'Arcimoto World Headquarters',
                'city': 'Eugene',
                'state': 'Oregon'
            },
            'coverage': 'internal',
            'model': 'FUV'
        },
        {
            'vin': 'DEV-7F7ATR31XMER00071',
            'location': {
                'name': 'Arcimoto World Headquarters',
                'city': 'Eugene',
                'state': 'Oregon'
            },
            'coverage': 'pilot',
            'model': 'FUV'
        },
        {
            'vin': 'DEV-7F7ATR31XMER00085',
            'location': {
                'name': 'Arcimoto Rental Facility [Eugene]',
                'city': 'Eugene',
                'state': 'Oregon'
            },
            'coverage': 'rental',
            'model': 'FUV'
        },
        {
            'vin': 'DEV-7F7ATR31XMER00099',
            'location': {
                'name': 'Arcimoto Rental Facility [Orlando]',
                'city': 'Orlando',
                'state': 'Florida'
            },
            'coverage': 'rental',
            'model': 'FUV'
        },
        {
            'vin': 'DEV-7F7ATR31XMER00135',
            'location': {
                'name': 'Arcimoto Rental Facility [Eugene]',
                'city': 'Eugene',
                'state': 'Oregon'
            },
            'coverage': 'rental',
            'model': 'FUV'
        }
    ]}
    vehicles_telemetry_data = [
        {
            'odometer': [

            ],
            'start': '2021-08-01 00:00:00',
            'vin': 'DEV-7F7ADR310MER00013',
            'end': '2021-08-31 23:59:59'
        },
        {
            'odometer': [
                {
                    'point': 685.6207614000001,
                    'time': '2021-08-22T00:09:00Z'
                },
                {
                    'point': 710.4693876900001,
                    'time': '2021-08-31T22:56:00Z'
                }
            ],
            'start': '2021-08-01 00:00:00',
            'vin': 'DEV-7F7ADR311LER00004',
            'end': '2021-08-31 23:59:59'
        },
        {
            'odometer': [

            ],
            'start': '2021-08-01 00:00:00',
            'vin': 'DEV-7F7ADR311MER00005',
            'end': '2021-08-31 23:59:59'
        },
        {
            'odometer': [

            ],
            'start': '2021-08-01 00:00:00',
            'vin': 'DEV-7F7ADR311MER00019',
            'end': '2021-08-31 23:59:59'
        },
        {
            'odometer': [

            ],
            'start': '2021-08-01 00:00:00',
            'vin': 'DEV-7F7ADR311MER00022',
            'end': '2021-08-31 23:59:59'
        },
        {
            'odometer': [

            ],
            'start': '2021-08-01 00:00:00',
            'vin': 'DEV-7F7ADR312MER00014',
            'end': '2021-08-31 23:59:59'
        },
        {
            'odometer': [

            ],
            'start': '2021-08-01 00:00:00',
            'vin': 'DEV-7F7ADR313LER00005',
            'end': '2021-08-31 23:59:59'
        },
        {
            'odometer': [

            ],
            'start': '2021-08-01 00:00:00',
            'vin': 'DEV-7F7ADR313MER00006',
            'end': '2021-08-31 23:59:59'
        },
        {
            'odometer': [

            ],
            'start': '2021-08-01 00:00:00',
            'vin': 'DEV-7F7ADR314MER00001',
            'end': '2021-08-31 23:59:59'
        },
        {
            'odometer': [

            ],
            'start': '2021-08-01 00:00:00',
            'vin': 'DEV-7F7ADR314MER00015',
            'end': '2021-08-31 23:59:59'
        },
        {
            'odometer': [
                {
                    'point': 197.49655864,
                    'time': '2021-08-23T21:23:00Z'
                },
                {
                    'point': 197.55869574,
                    'time': '2021-08-31T15:03:00Z'
                }
            ],
            'start': '2021-08-01 00:00:00',
            'vin': 'DEV-7F7ADR315LER00006',
            'end': '2021-08-31 23:59:59'
        },
        {
            'odometer': [

            ],
            'start': '2021-08-01 00:00:00',
            'vin': 'DEV-7F7ADR315MER00007',
            'end': '2021-08-31 23:59:59'
        },
        {
            'odometer': [

            ],
            'start': '2021-08-01 00:00:00',
            'vin': 'DEV-7F7ADR315MER00010',
            'end': '2021-08-31 23:59:59'
        },
        {
            'odometer': [
                {
                    'point': 2626.66570491,
                    'time': '2021-08-23T19:38:00Z'
                },
                {
                    'point': 2626.7216283000002,
                    'time': '2021-08-23T21:06:00Z'
                }
            ],
            'start': '2021-08-01 00:00:00',
            'vin': 'DEV-7F7ADR316LER00001',
            'end': '2021-08-31 23:59:59'
        },
        {
            'odometer': [

            ],
            'start': '2021-08-01 00:00:00',
            'vin': 'DEV-7F7ADR316MER00016',
            'end': '2021-08-31 23:59:59'
        },
        {
            'odometer': [

            ],
            'start': '2021-08-01 00:00:00',
            'vin': 'DEV-7F7ADR317MER00008',
            'end': '2021-08-31 23:59:59'
        },
        {
            'odometer': [

            ],
            'start': '2021-08-01 00:00:00',
            'vin': 'DEV-7F7ADR317MER00011',
            'end': '2021-08-31 23:59:59'
        },
        {
            'odometer': [
                {
                    'point': 203.87803881000002,
                    'time': '2021-08-24T20:36:00Z'
                },
                {
                    'point': 210.18495446,
                    'time': '2021-08-30T18:58:00Z'
                }
            ],
            'start': '2021-08-01 00:00:00',
            'vin': 'DEV-7F7ADR318LER00002',
            'end': '2021-08-31 23:59:59'
        },
        {
            'odometer': [

            ],
            'start': '2021-08-01 00:00:00',
            'vin': 'DEV-7F7ADR318MER00017',
            'end': '2021-08-31 23:59:59'
        },
        {
            'odometer': [

            ],
            'start': '2021-08-01 00:00:00',
            'vin': 'DEV-7F7ADR318MER00020',
            'end': '2021-08-31 23:59:59'
        },
        {
            'odometer': [

            ],
            'start': '2021-08-01 00:00:00',
            'vin': 'DEV-7F7ADR319MER00009',
            'end': '2021-08-31 23:59:59'
        },
        {
            'odometer': [

            ],
            'start': '2021-08-01 00:00:00',
            'vin': 'DEV-7F7ADR319MER00012',
            'end': '2021-08-31 23:59:59'
        },
        {
            'odometer': [
                {
                    'point': 0.22369355999999999,
                    'time': '2021-08-24T22:57:00Z'
                },
                {
                    'point': 0.27961695000000003,
                    'time': '2021-08-24T22:59:00Z'
                }
            ],
            'start': '2021-08-01 00:00:00',
            'vin': 'DEV-7F7ADR31XLER00003',
            'end': '2021-08-31 23:59:59'
        },
        {
            'odometer': [
                {
                    'point': 38.89782460000001,
                    'time': '2021-08-23T21:17:00Z'
                },
                {
                    'point': 38.94132057,
                    'time': '2021-08-30T21:45:00Z'
                }
            ],
            'start': '2021-08-01 00:00:00',
            'vin': 'DEV-7F7ADR31XMER00004',
            'end': '2021-08-31 23:59:59'
        },
        {
            'odometer': [

            ],
            'start': '2021-08-01 00:00:00',
            'vin': 'DEV-7F7ADR31XMER00018',
            'end': '2021-08-31 23:59:59'
        },
        {
            'odometer': [

            ],
            'start': '2021-08-01 00:00:00',
            'vin': 'DEV-7F7ADR31XMER00021',
            'end': '2021-08-31 23:59:59'
        },
        {
            'odometer': [

            ],
            'start': '2021-08-01 00:00:00',
            'vin': 'DEV-7F7AER318MER00001',
            'end': '2021-08-31 23:59:59'
        },
        {
            'odometer': [
                {
                    'point': 325.00188783999994,
                    'time': '2021-08-24T20:28:00Z'
                },
                {
                    'point': 325.01431526,
                    'time': '2021-08-24T20:57:00Z'
                }
            ],
            'start': '2021-08-01 00:00:00',
            'vin': 'DEV-7F7ARR311MER00006',
            'end': '2021-08-31 23:59:59'
        },
        {
            'odometer': [
                {
                    'point': 447.85314825,
                    'time': '2021-08-22T00:26:00Z'
                },
                {
                    'point': 504.62154067290004,
                    'time': '2021-08-27T18:38:00Z'
                }
            ],
            'start': '2021-08-01 00:00:00',
            'vin': 'DEV-7F7ARR312MER00001',
            'end': '2021-08-31 23:59:59'
        },
        {
            'odometer': [
                {
                    'point': 585.31905458,
                    'time': '2021-08-24T20:27:00Z'
                },
                {
                    'point': 585.3874053900001,
                    'time': '2021-08-27T19:04:00Z'
                }
            ],
            'start': '2021-08-01 00:00:00',
            'vin': 'DEV-7F7ARR313MER00007',
            'end': '2021-08-31 23:59:59'
        },
        {
            'odometer': [

            ],
            'start': '2021-08-01 00:00:00',
            'vin': 'DEV-7F7ARR314LER00001',
            'end': '2021-08-31 23:59:59'
        },
        {
            'odometer': [

            ],
            'start': '2021-08-01 00:00:00',
            'vin': 'DEV-7F7ARR314MER00002',
            'end': '2021-08-31 23:59:59'
        },
        {
            'odometer': [

            ],
            'start': '2021-08-01 00:00:00',
            'vin': 'DEV-7F7ARR316LER00002',
            'end': '2021-08-31 23:59:59'
        },
        {
            'odometer': [

            ],
            'start': '2021-08-01 00:00:00',
            'vin': 'DEV-7F7ARR316MER00003',
            'end': '2021-08-31 23:59:59'
        },
        {
            'odometer': [

            ],
            'start': '2021-08-01 00:00:00',
            'vin': 'DEV-7F7ARR318LER00003',
            'end': '2021-08-31 23:59:59'
        },
        {
            'odometer': [

            ],
            'start': '2021-08-01 00:00:00',
            'vin': 'DEV-7F7ARR318MER00004',
            'end': '2021-08-31 23:59:59'
        },
        {
            'odometer': [

            ],
            'start': '2021-08-01 00:00:00',
            'vin': 'DEV-7F7ARR31XLER00004',
            'end': '2021-08-31 23:59:59'
        },
        {
            'odometer': [
                {
                    'point': 80.92114532999999,
                    'time': '2021-08-24T14:23:00Z'
                },
                {
                    'point': 80.95842759,
                    'time': '2021-08-25T00:04:00Z'
                }
            ],
            'start': '2021-08-01 00:00:00',
            'vin': 'DEV-7F7ARR31XMER00005',
            'end': '2021-08-31 23:59:59'
        },
        {
            'odometer': [

            ],
            'start': '2021-08-01 00:00:00',
            'vin': 'DEV-7F7ATR310MER00029',
            'end': '2021-08-31 23:59:59'
        },
        {
            'odometer': [
                {
                    'point': 1424.69806993,
                    'time': '2021-08-22T15:44:00Z'
                },
                {
                    'point': 1756.84572427,
                    'time': '2021-08-30T22:57:00Z'
                }
            ],
            'start': '2021-08-01 00:00:00',
            'vin': 'DEV-7F7ATR310MER00077',
            'end': '2021-08-31 23:59:59'
        },
        {
            'odometer': [

            ],
            'start': '2021-08-01 00:00:00',
            'vin': 'DEV-7F7ATR310MER00080',
            'end': '2021-08-31 23:59:59'
        },
        {
            'odometer': [
                {
                    'point': 280.28181697,
                    'time': '2021-08-22T18:03:00Z'
                },
                {
                    'point': 446.73468045000004,
                    'time': '2021-08-31T22:53:00Z'
                }
            ],
            'start': '2021-08-01 00:00:00',
            'vin': 'DEV-7F7ATR310MER00130',
            'end': '2021-08-31 23:59:59'
        },
        {
            'odometer': [
                {
                    'point': 143.64233407,
                    'time': '2021-08-25T13:43:00Z'
                },
                {
                    'point': 143.64854778,
                    'time': '2021-08-25T13:44:00Z'
                }
            ],
            'start': '2021-08-01 00:00:00',
            'vin': 'DEV-7F7ATR311LER00023',
            'end': '2021-08-31 23:59:59'
        },
        {
            'odometer': [

            ],
            'start': '2021-08-01 00:00:00',
            'vin': 'DEV-7F7ATR311LER00085',
            'end': '2021-08-31 23:59:59'
        },
        {
            'odometer': [

            ],
            'start': '2021-08-01 00:00:00',
            'vin': 'DEV-7F7ATR311MER00055',
            'end': '2021-08-31 23:59:59'
        },
        {
            'odometer': [

            ],
            'start': '2021-08-01 00:00:00',
            'vin': 'DEV-7F7ATR311MER00072',
            'end': '2021-08-31 23:59:59'
        },
        {
            'odometer': [
                {
                    'point': 1827.25948599,
                    'time': '2021-08-22T16:22:00Z'
                },
                {
                    'point': 2076.5038215100008,
                    'time': '2021-08-29T22:19:00Z'
                }
            ],
            'start': '2021-08-01 00:00:00',
            'vin': 'DEV-7F7ATR311MER00086',
            'end': '2021-08-31 23:59:59'
        },
        {
            'odometer': [

            ],
            'start': '2021-08-01 00:00:00',
            'vin': 'DEV-7F7ATR311MER00122',
            'end': '2021-08-31 23:59:59'
        },
        {
            'odometer': [

            ],
            'start': '2021-08-01 00:00:00',
            'vin': 'DEV-7F7ATR311MER00136',
            'end': '2021-08-31 23:59:59'
        },
        {
            'odometer': [
                {
                    'point': 5522.63360122,
                    'time': '2021-08-30T21:18:00Z'
                },
                {
                    'point': 5588.19445543,
                    'time': '2021-08-31T23:37:00Z'
                }
            ],
            'start': '2021-08-01 00:00:00',
            'vin': 'DEV-7F7ATR312LER00015',
            'end': '2021-08-31 23:59:59'
        },
        {
            'odometer': [
                {
                    'point': 5100.9028898100005,
                    'time': '2021-08-29T18:28:00Z'
                },
                {
                    'point': 5101.01473659,
                    'time': '2021-08-29T18:43:00Z'
                }
            ],
            'start': '2021-08-01 00:00:00',
            'vin': 'DEV-7F7ATR312LER00046',
            'end': '2021-08-31 23:59:59'
        },
        {
            'odometer': [
                {
                    'point': 555.65480304,
                    'time': '2021-08-22T00:00:00Z'
                },
                {
                    'point': 774.9552700700001,
                    'time': '2021-08-31T20:47:00Z'
                }
            ],
            'start': '2021-08-01 00:00:00',
            'vin': 'DEV-7F7ATR312MER00131',
            'end': '2021-08-31 23:59:59'
        },
        {
            'odometer': [
                {
                    'point': 5.30029463,
                    'time': '2021-08-23T20:23:00Z'
                },
                {
                    'point': 163.87417383000002,
                    'time': '2021-08-30T22:42:00Z'
                }
            ],
            'start': '2021-08-01 00:00:00',
            'vin': 'DEV-7F7ATR312MER00159',
            'end': '2021-08-31 23:59:59'
        },
        {
            'odometer': [

            ],
            'start': '2021-08-01 00:00:00',
            'vin': 'DEV-7F7ATR313LER00010',
            'end': '2021-08-31 23:59:59'
        },
        {
            'odometer': [

            ],
            'start': '2021-08-01 00:00:00',
            'vin': 'DEV-7F7ATR313LER00038',
            'end': '2021-08-31 23:59:59'
        },
        {
            'odometer': [

            ],
            'start': '2021-08-01 00:00:00',
            'vin': 'DEV-7F7ATR313LER00086',
            'end': '2021-08-31 23:59:59'
        },
        {
            'odometer': [

            ],
            'start': '2021-08-01 00:00:00',
            'vin': 'DEV-7F7ATR313MER00073',
            'end': '2021-08-31 23:59:59'
        },
        {
            'odometer': [

            ],
            'start': '2021-08-01 00:00:00',
            'vin': 'DEV-7F7ATR313MER00087',
            'end': '2021-08-31 23:59:59'
        },
        {
            'odometer': [
                {
                    'point': 2206.78667908,
                    'time': '2021-08-22T00:11:00Z'
                },
                {
                    'point': 2488.92639534,
                    'time': '2021-08-31T21:16:00Z'
                }
            ],
            'start': '2021-08-01 00:00:00',
            'vin': 'DEV-7F7ATR313MER00090',
            'end': '2021-08-31 23:59:59'
        },
        {
            'odometer': [
                {
                    'point': 5.30029463,
                    'time': '2021-08-23T19:38:00Z'
                },
                {
                    'point': 5.3437906,
                    'time': '2021-08-31T20:09:00Z'
                }
            ],
            'start': '2021-08-01 00:00:00',
            'vin': 'DEV-7F7ATR313MER00137',
            'end': '2021-08-31 23:59:59'
        },
        {
            'odometer': [
                {
                    'point': 6.71702051,
                    'time': '2021-08-23T20:30:00Z'
                },
                {
                    'point': 61.36659996,
                    'time': '2021-08-30T22:45:00Z'
                }
            ],
            'start': '2021-08-01 00:00:00',
            'vin': 'DEV-7F7ATR313MER00154',
            'end': '2021-08-31 23:59:59'
        },
        {
            'odometer': [

            ],
            'start': '2021-08-01 00:00:00',
            'vin': 'DEV-7F7ATR314KER00015',
            'end': '2021-08-31 23:59:59'
        },
        {
            'odometer': [
                {
                    'point': 2835.65141334,
                    'time': '2021-08-22T20:48:00Z'
                },
                {
                    'point': 2915.56593765,
                    'time': '2021-08-31T21:39:00Z'
                }
            ],
            'start': '2021-08-01 00:00:00',
            'vin': 'DEV-7F7ATR314KER00032',
            'end': '2021-08-31 23:59:59'
        },
        {
            'odometer': [
                {
                    'point': 1382.82387824,
                    'time': '2021-08-24T19:27:00Z'
                },
                {
                    'point': 1399.48904846,
                    'time': '2021-08-30T03:51:00Z'
                }
            ],
            'start': '2021-08-01 00:00:00',
            'vin': 'DEV-7F7ATR314LER00047',
            'end': '2021-08-31 23:59:59'
        },
        {
            'odometer': [
                {
                    'point': 3454.99674388,
                    'time': '2021-08-23T11:36:00Z'
                },
                {
                    'point': 3510.30497659,
                    'time': '2021-08-30T19:14:00Z'
                }
            ],
            'start': '2021-08-01 00:00:00',
            'vin': 'DEV-7F7ATR314LER00081',
            'end': '2021-08-31 23:59:59'
        },
        {
            'odometer': [

            ],
            'start': '2021-08-01 00:00:00',
            'vin': 'DEV-7F7ATR314MER00082',
            'end': '2021-08-31 23:59:59'
        },
        {
            'odometer': [
                {
                    'point': 369.12544255,
                    'time': '2021-08-22T18:20:00Z'
                },
                {
                    'point': 451.33903956,
                    'time': '2021-08-31T20:51:00Z'
                }
            ],
            'start': '2021-08-01 00:00:00',
            'vin': 'DEV-7F7ATR314MER00129',
            'end': '2021-08-31 23:59:59'
        },
        {
            'odometer': [
                {
                    'point': 104.52081591000001,
                    'time': '2021-08-23T15:56:00Z'
                },
                {
                    'point': 178.71251331000002,
                    'time': '2021-08-31T22:26:00Z'
                }
            ],
            'start': '2021-08-01 00:00:00',
            'vin': 'DEV-7F7ATR314MER00132',
            'end': '2021-08-31 23:59:59'
        },
        {
            'odometer': [
                {
                    'point': 95.20025091000001,
                    'time': '2021-08-22T13:14:00Z'
                },
                {
                    'point': 483.84917027999995,
                    'time': '2021-08-31T16:47:00Z'
                }
            ],
            'start': '2021-08-01 00:00:00',
            'vin': 'DEV-7F7ATR314MER00163',
            'end': '2021-08-31 23:59:59'
        },
        {
            'odometer': [

            ],
            'start': '2021-08-01 00:00:00',
            'vin': 'DEV-7F7ATR315LER00011',
            'end': '2021-08-31 23:59:59'
        },
        {
            'odometer': [
                {
                    'point': 1143.09894644,
                    'time': '2021-08-23T16:04:00Z'
                },
                {
                    'point': 1208.24348208,
                    'time': '2021-08-29T12:48:00Z'
                }
            ],
            'start': '2021-08-01 00:00:00',
            'vin': 'DEV-7F7ATR315LER00042',
            'end': '2021-08-31 23:59:59'
        },
        {
            'odometer': [
                {
                    'point': 3028.50633061,
                    'time': '2021-08-22T01:14:00Z'
                },
                {
                    'point': 3138.0540379100003,
                    'time': '2021-08-31T04:59:00Z'
                }
            ],
            'start': '2021-08-01 00:00:00',
            'vin': 'DEV-7F7ATR315LER00087',
            'end': '2021-08-31 23:59:59'
        },
        {
            'odometer': [

            ],
            'start': '2021-08-01 00:00:00',
            'vin': 'DEV-7F7ATR315MER00074',
            'end': '2021-08-31 23:59:59'
        },
        {
            'odometer': [

            ],
            'start': '2021-08-01 00:00:00',
            'vin': 'DEV-7F7ATR315MER00091',
            'end': '2021-08-31 23:59:59'
        },
        {
            'odometer': [
                {
                    'point': 5.39350028,
                    'time': '2021-08-27T16:23:00Z'
                },
                {
                    'point': 5.840887400000001,
                    'time': '2021-08-31T22:20:00Z'
                }
            ],
            'start': '2021-08-01 00:00:00',
            'vin': 'DEV-7F7ATR315MER00138',
            'end': '2021-08-31 23:59:59'
        },
        {
            'odometer': [
                {
                    'point': 5.44320996,
                    'time': '2021-08-23T20:23:00Z'
                },
                {
                    'point': 75.93774991,
                    'time': '2021-08-30T22:55:00Z'
                }
            ],
            'start': '2021-08-01 00:00:00',
            'vin': 'DEV-7F7ATR315MER00155',
            'end': '2021-08-31 23:59:59'
        },
        {
            'odometer': [
                {
                    'point': 1745.431139,
                    'time': '2021-08-23T13:40:00Z'
                },
                {
                    'point': 1750.19705457,
                    'time': '2021-08-30T21:03:00Z'
                }
            ],
            'start': '2021-08-01 00:00:00',
            'vin': 'DEV-7F7ATR316LER00082',
            'end': '2021-08-31 23:59:59'
        },
        {
            'odometer': [

            ],
            'start': '2021-08-01 00:00:00',
            'vin': 'DEV-7F7ATR316MER00097',
            'end': '2021-08-31 23:59:59'
        },
        {
            'odometer': [

            ],
            'start': '2021-08-01 00:00:00',
            'vin': 'DEV-7F7ATR316MER00102',
            'end': '2021-08-31 23:59:59'
        },
        {
            'odometer': [
                {
                    'point': 262.57274347,
                    'time': '2021-08-22T19:33:00Z'
                },
                {
                    'point': 451.04699519,
                    'time': '2021-08-31T01:38:00Z'
                }
            ],
            'start': '2021-08-01 00:00:00',
            'vin': 'DEV-7F7ATR316MER00133',
            'end': '2021-08-31 23:59:59'
        },
        {
            'odometer': [
                {
                    'point': 92.18660156000001,
                    'time': '2021-08-22T16:17:00Z'
                },
                {
                    'point': 104.96820303000001,
                    'time': '2021-08-30T19:23:00Z'
                }
            ],
            'start': '2021-08-01 00:00:00',
            'vin': 'DEV-7F7ATR316MER00164',
            'end': '2021-08-31 23:59:59'
        },
        {
            'odometer': [
                {
                    'point': 2416.62366578,
                    'time': '2021-08-22T21:26:00Z'
                },
                {
                    'point': 2524.1084213599997,
                    'time': '2021-08-31T19:07:00Z'
                }
            ],
            'start': '2021-08-01 00:00:00',
            'vin': 'DEV-7F7ATR317LER00088',
            'end': '2021-08-31 23:59:59'
        },
        {
            'odometer': [

            ],
            'start': '2021-08-01 00:00:00',
            'vin': 'DEV-7F7ATR317MER00027',
            'end': '2021-08-31 23:59:59'
        },
        {
            'odometer': [

            ],
            'start': '2021-08-01 00:00:00',
            'vin': 'DEV-7F7ATR317MER00030',
            'end': '2021-08-31 23:59:59'
        },
        {
            'odometer': [

            ],
            'start': '2021-08-01 00:00:00',
            'vin': 'DEV-7F7ATR317MER00075',
            'end': '2021-08-31 23:59:59'
        },
        {
            'odometer': [
                {
                    'point': 1696.5975921099998,
                    'time': '2021-08-22T00:03:00Z'
                },
                {
                    'point': 2022.1276453,
                    'time': '2021-08-31T23:59:00Z'
                }
            ],
            'start': '2021-08-01 00:00:00',
            'vin': 'DEV-7F7ATR317MER00089',
            'end': '2021-08-31 23:59:59'
        },
        {
            'odometer': [
                {
                    'point': 2415.75374638,
                    'time': '2021-08-22T15:40:00Z'
                },
                {
                    'point': 2721.26322595,
                    'time': '2021-08-31T20:17:00Z'
                }
            ],
            'start': '2021-08-01 00:00:00',
            'vin': 'DEV-7F7ATR317MER00092',
            'end': '2021-08-31 23:59:59'
        },
        {
            'odometer': [
                {
                    'point': 5.983802730000001,
                    'time': '2021-08-23T21:21:00Z'
                },
                {
                    'point': 6.449830980000001,
                    'time': '2021-08-31T22:22:00Z'
                }
            ],
            'start': '2021-08-01 00:00:00',
            'vin': 'DEV-7F7ATR317MER00139',
            'end': '2021-08-31 23:59:59'
        },
        {
            'odometer': [

            ],
            'start': '2021-08-01 00:00:00',
            'vin': 'DEV-7F7ATR317MER00156',
            'end': '2021-08-31 23:59:59'
        },
        {
            'odometer': [

            ],
            'start': '2021-08-01 00:00:00',
            'vin': 'DEV-7F7ATR318KER00003',
            'end': '2021-08-31 23:59:59'
        },
        {
            'odometer': [
                {
                    'point': 435.63699439000004,
                    'time': '2021-08-23T03:16:00Z'
                },
                {
                    'point': 509.69199017,
                    'time': '2021-08-31T19:10:00Z'
                }
            ],
            'start': '2021-08-01 00:00:00',
            'vin': 'DEV-7F7ATR318LER00052',
            'end': '2021-08-31 23:59:59'
        },
        {
            'odometer': [

            ],
            'start': '2021-08-01 00:00:00',
            'vin': 'DEV-7F7ATR318LER00083',
            'end': '2021-08-31 23:59:59'
        },
        {
            'odometer': [

            ],
            'start': '2021-08-01 00:00:00',
            'vin': 'DEV-7F7ATR318MER00084',
            'end': '2021-08-31 23:59:59'
        },
        {
            'odometer': [

            ],
            'start': '2021-08-01 00:00:00',
            'vin': 'DEV-7F7ATR318MER00098',
            'end': '2021-08-31 23:59:59'
        },
        {
            'odometer': [
                {
                    'point': 5.4680648000000005,
                    'time': '2021-08-23T19:30:00Z'
                },
                {
                    'point': 11.9303232,
                    'time': '2021-08-30T23:15:00Z'
                }
            ],
            'start': '2021-08-01 00:00:00',
            'vin': 'DEV-7F7ATR318MER00134',
            'end': '2021-08-31 23:59:59'
        },
        {
            'odometer': [
                {
                    'point': 1084.42909662,
                    'time': '2021-08-24T21:52:00Z'
                },
                {
                    'point': 1195.71664272,
                    'time': '2021-08-31T21:54:00Z'
                }
            ],
            'start': '2021-08-01 00:00:00',
            'vin': 'DEV-7F7ATR319KER00009',
            'end': '2021-08-31 23:59:59'
        },
        {
            'odometer': [

            ],
            'start': '2021-08-01 00:00:00',
            'vin': 'DEV-7F7ATR319LER00044',
            'end': '2021-08-31 23:59:59'
        },
        {
            'odometer': [

            ],
            'start': '2021-08-01 00:00:00',
            'vin': 'DEV-7F7ATR319MER00028',
            'end': '2021-08-31 23:59:59'
        },
        {
            'odometer': [

            ],
            'start': '2021-08-01 00:00:00',
            'vin': 'DEV-7F7ATR319MER00031',
            'end': '2021-08-31 23:59:59'
        },
        {
            'odometer': [
                {
                    'point': 735.5852035099999,
                    'time': '2021-08-30T14:18:00Z'
                },
                {
                    'point': 735.5852035099999,
                    'time': '2021-08-30T14:18:00Z'
                }
            ],
            'start': '2021-08-01 00:00:00',
            'vin': 'DEV-7F7ATR319MER00076',
            'end': '2021-08-31 23:59:59'
        },
        {
            'odometer': [

            ],
            'start': '2021-08-01 00:00:00',
            'vin': 'DEV-7F7ATR31XKER00004',
            'end': '2021-08-31 23:59:59'
        },
        {
            'odometer': [
                {
                    'point': 3257.77358848,
                    'time': '2021-08-26T22:55:00Z'
                },
                {
                    'point': 3257.77358848,
                    'time': '2021-08-31T23:59:00Z'
                }
            ],
            'start': '2021-08-01 00:00:00',
            'vin': 'DEV-7F7ATR31XLER00084',
            'end': '2021-08-31 23:59:59'
        },
        {
            'odometer': [

            ],
            'start': '2021-08-01 00:00:00',
            'vin': 'DEV-7F7ATR31XLER00117',
            'end': '2021-08-31 23:59:59'
        },
        {
            'odometer': [

            ],
            'start': '2021-08-01 00:00:00',
            'vin': 'DEV-7F7ATR31XMER00071',
            'end': '2021-08-31 23:59:59'
        },
        {
            'odometer': [
                {
                    'point': 1805.40586792,
                    'time': '2021-08-22T16:26:00Z'
                },
                {
                    'point': 2048.0450297100006,
                    'time': '2021-08-31T23:05:00Z'
                }
            ],
            'start': '2021-08-01 00:00:00',
            'vin': 'DEV-7F7ATR31XMER00085',
            'end': '2021-08-31 23:59:59'
        },
        {
            'odometer': [

            ],
            'start': '2021-08-01 00:00:00',
            'vin': 'DEV-7F7ATR31XMER00099',
            'end': '2021-08-31 23:59:59'
        },
        {
            'odometer': [
                {
                    'point': 5.59855271,
                    'time': '2021-08-30T15:50:00Z'
                },
                {
                    'point': 7.3321778,
                    'time': '2021-08-30T22:30:00Z'
                }
            ],
            'start': '2021-08-01 00:00:00',
            'vin': 'DEV-7F7ATR31XMER00135',
            'end': '2021-08-31 23:59:59'
        }
    ]
    args = {
        'vehicles_db_data': vehicles_db_data,
        'vehicles_telemetry_data': vehicles_telemetry_data
    }

    def test_yrisk_output_assemble_success(self):
        self.assertIsInstance(yrisk_functions.output_assemble(self.args), dict)

    # test errors
    def test_yrisk_output_assemble_error_input_null_vehicles_db_data(self):
        args = copy.deepcopy(self.args)
        args['vehicles_db_data'] = None
        with self.assertRaises(ArcimotoArgumentError):
            yrisk_functions.output_assemble(args)

    def test_yrisk_output_assemble_error_input_null_vehicles_telemetry_data(self):
        args = copy.deepcopy(self.args)
        args['vehicles_telemetry_data'] = None
        with self.assertRaises(ArcimotoArgumentError):
            yrisk_functions.output_assemble(args)

    def test_yrisk_output_assemble_error_input_empty_vehicles_telemetry_data(self):
        args = copy.deepcopy(self.args)
        args['vehicles_telemetry_data'] = []
        with self.assertRaises(ArcimotoArgumentError):
            yrisk_functions.output_assemble(args)

    def test_yrisk_output_assemble_error_input_invalid_type_vehicles_db_data(self):
        args = copy.deepcopy(self.args)
        args['vehicles_db_data'] = 'not a dictionary'
        with self.assertRaises(ArcimotoArgumentError):
            yrisk_functions.output_assemble(args)

    def test_yrisk_output_assemble_error_input_invalid_type_vehicles_telemetry_data(self):
        args = copy.deepcopy(self.args)
        args['vehicles_telemetry_data'] = 'not a list'
        with self.assertRaises(ArcimotoArgumentError):
            yrisk_functions.output_assemble(args)


@arcimoto.runtime.handler
def test_yrisk_output_assemble():
    return arcimoto.tests.handle_test_result(unittest.TextTestRunner().run(
        unittest.TestLoader().loadTestsFromTestCase(YriskOutputAssembleTestCase)
    ))


lambda_handler = test_yrisk_output_assemble
