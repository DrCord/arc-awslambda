import logging
from influxdb import InfluxDBClient

from arcimoto.exceptions import *
import arcimoto.runtime
import arcimoto.user
import arcimoto.db

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

arcimoto.args.register({
    'fleet_name': {
        'type': 'string',
        'nullable': True,
        'default': 'Arcimoto'
    }
})

# config for sending queries to Influx
TELEMETRY_DB_NAME = 'amtelemetry'


@arcimoto.runtime.handler
def fleets_statistics_get(fleet_name):
    '''
    gets the aggregated odometer reading and number of vehicles for fleet by name
    also returns the mpge which is probably needed for any relevant calculations
    '''

    global logger

    cursor = arcimoto.db.get_cursor()

    output = {
        'fleet_name': fleet_name,
        'total_mileage': 0
    }
    data = {
        'id': None,
        'vehicles': []
    }
    query = (
        'SELECT id '
        'FROM vehicle_group '
        'WHERE name=%s'
    )
    cursor.execute(query, [fleet_name])
    if cursor.rowcount == 0:
        raise ArcimotoArgumentError(f'Invalid Fleet Name: {fleet_name}')
    row = cursor.fetchone()
    data['id'] = row['id']

    query = (
        'SELECT v.vin '
        'FROM vehicle v '
        'LEFT JOIN vehicle_join_vehicle_group vj '
        'ON v.vin=vj.vin '
        'WHERE vj.group_id=%s'
    )
    cursor.execute(query, [data['id']])
    for row in cursor:
        data['vehicles'].append(row['vin'])

    # open influxdb client
    client = InfluxDBClient(host=influx_ip_get(), port=90)
    client.switch_database(TELEMETRY_DB_NAME)

    # fetch stats (odometer) from influx for all vehicles in fleet
    output['total_mileage'] = vehicles_odometer_get(client, data['vehicles'])

    return output


def vehicles_odometer_get(client, vins):
    '''
    query influxdb for latest odometer readings for list of vins
    add together and round to int
    '''

    total_kilometers = 0

    query = (
        'SELECT odometer '
        'FROM telemetry '
        'GROUP BY * '
        'ORDER BY time '
        'DESC LIMIT 1'
    )
    results = client.query(query)
    for vin in vins:
        points = results.get_points(tags={'vin': vin})
        for point in points:
            odometer = point.get('odometer', 0)
            if odometer:
                total_kilometers = total_kilometers + odometer

    # convert kilometers to miles and round to int
    total_mileage = int(round(total_kilometers * 0.62137))

    return total_mileage


def influx_ip_get():
    try:
        env = arcimoto.runtime.get_env()
        influx_ip = arcimoto.runtime.get_secret(f'telemetry.influxdb.ip.{env}').get('ip', None)
        if influx_ip is None:
            raise ArcimotoException(f'Unable to get IndluxDB IP for {env}')
        return influx_ip
    except Exception as e:
        raise ArcimotoException(e)


lambda_handler = fleets_statistics_get
