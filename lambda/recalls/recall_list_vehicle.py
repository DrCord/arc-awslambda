import logging

from arcimoto.exceptions import *
import arcimoto.runtime
import arcimoto.args
import arcimoto.user
import arcimoto.db

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

arcimoto.args.register({
    'vin': {
        'type': 'string',
        'nullable': True
    },
    'get_recall_data': {
        'type': 'boolean',
        'nullable': True
    },
    'get_deleted_recalls': {
        'type': 'boolean',
        'nullable': True
    }
})


@arcimoto.runtime.handler
def recall_list_vehicle(vin=None, get_recall_data=False, get_deleted_recalls=False):
    global logger

    cursor = arcimoto.db.get_cursor()

    models_query = (
        'SELECT vm.model_name, vm.letter_code '
        'FROM vehicle_model AS vm '
        'LEFT JOIN vehicle_platform vp '
        'ON vm.platform_id = vp.id '
        "WHERE vp.platform_name = 'FUV 1.0'"
    )
    cursor.execute(models_query)
    models = {}
    # create lookup dict letter_code -> model_name
    for record in cursor:
        models[record['letter_code']] = record['model_name']

    query = (
        'SELECT vr.id, vr.recall_id, vr.service_date, vr.service_reference, vr.vin '
        'FROM vehicle_recalls AS vr '
    )

    if get_deleted_recalls:
        query, params = prepare_get_deleted_recalls_query_and_params(query, vin)
    else:
        query, params = prepare_recalls_query_and_params(query, vin)
    cursor.execute(query, params)

    vehicle_recalls = []
    for record in cursor:
        recall_vin = record['vin']
        vehicle_recalls.append(
            {
                'vehicle_recall_id': record['id'],
                'recall_id': record['recall_id'],
                'service_date': arcimoto.db.datetime_record_output(record['service_date']),
                'service_reference': record['service_reference'],
                'vin': recall_vin,
                'model': models.get(recall_vin[-13], 'Other')
            }
        )

    if get_recall_data:
        for vehicle_recall in vehicle_recalls:
            query = (
                'SELECT id, mfr_campaign_id, country, title, description, nhtsa_number, date, remedy_id, safety_recall, safety_description, status '
                'FROM recalls '
                'WHERE id = %s '
                'ORDER BY id ASC'
            )
            cursor.execute(query, [vehicle_recall['recall_id']])
            for record in cursor:
                vehicle_recall['recall'] = {
                    'id': record['id'],
                    'mfr_campaign_id': record['mfr_campaign_id'],
                    'country': record['country'],
                    'title': record['title'],
                    'description': record['description'],
                    'nhtsa_number': record['nhtsa_number'],
                    'date': arcimoto.db.datetime_record_output(record['date']),
                    'remedy_id': record['remedy_id'],
                    'safety_recall': record['safety_recall'],
                    'safety_description': record['safety_description'],
                    'status': record['status']
                }

            if vehicle_recall['recall']['remedy_id'] is not None:
                query = (
                    'SELECT id, date, description '
                    'FROM recall_remedies '
                    'WHERE id = %s '
                    'ORDER BY id ASC'
                )
                cursor.execute(query, [vehicle_recall['recall']['remedy_id']])
                for record in cursor:
                    vehicle_recall['recall']['remedy'] = {
                        'id': record['id'],
                        'date': arcimoto.db.datetime_record_output(record['date']),
                        'description': record['description'],
                    }

    return {'vehicle_recalls': vehicle_recalls}


@arcimoto.user.require('recalls.recall.read')
def prepare_get_deleted_recalls_query_and_params(query, vin):
    params = []
    if vin is not None:
        query += 'WHERE vin = %s '
        params.append(vin)
    query += 'ORDER by id ASC'
    return (query, params)


def prepare_recalls_query_and_params(query, vin):
    query += (
        'LEFT JOIN recalls '
        'ON vr.recall_id = recalls.id '
        'WHERE recalls.status != \'deleted\' '
    )
    params = []
    if vin is not None:
        query += 'AND vin = %s '
        params.append(vin)
    query += 'ORDER BY vr.id ASC'
    return (query, params)


lambda_handler = recall_list_vehicle
