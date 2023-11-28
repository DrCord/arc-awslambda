import logging

from arcimoto.exceptions import *
import arcimoto.runtime
import arcimoto.db

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


@arcimoto.runtime.handler
def locations_countries_list():
    '''List all country's code corresponding name, ordered by country code ascending'''
    global logger

    cursor = arcimoto.db.get_cursor()
    try:
        query = (
            'SELECT country_code, country_name '
            'FROM countries '
            'ORDER BY country_code ASC'
        )
        cursor.execute(query)

        result = []
        for record in cursor:
            result.append(
                {
                    'country_code': record['country_code'],
                    'country_name': record['country_name']
                }
            )
    except Exception as e:
        raise ArcimotoException(f'Unable to get countries from db: {e}') from e

    return {'countries': result}


lambda_handler = locations_countries_list
