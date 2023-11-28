import logging
import json

from arcimoto.exceptions import *
import arcimoto.runtime
import arcimoto.user
import arcimoto.db

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

arcimoto.args.register({
    'recall_id': {
        'type': 'integer',
        'required': True,
        'min': 1
    },
    'get_additional_data': {
        'type': 'boolean',
        'nullable': True
    }
})


@arcimoto.runtime.handler
@arcimoto.user.require('recalls.recall.read')
def recall_get(recall_id, get_additional_data):
    global logger

    cursor = arcimoto.db.get_cursor()
    recall = {}
    query = ('SELECT '
             'id, '
             'mfr_campaign_id, '
             'country, '
             'title, '
             'description, '
             'nhtsa_number, '
             'date, '
             'remedy_id, '
             'safety_recall, '
             'safety_description, '
             'status '
             'FROM recalls '
             'WHERE id=%s'
             )
    cursor.execute(query, [recall_id])
    if cursor.rowcount != 1:
        raise Exception('Invalid recall_id')
    result = cursor.fetchone()
    recall = {
        'recall_id': result['id'],
        'mfr_campaign_id': result['mfr_campaign_id'],
        'country': result['country'],
        'title': result['title'],
        'description': result['description'],
        'nhtsa_number': result['nhtsa_number'],
        'date': arcimoto.db.datetime_record_output(result['date']),
        'remedy_id': result['remedy_id'],
        'safety_recall': result['safety_recall'],
        'safety_description': result['safety_description'],
        'status': result['status']
    }

    if get_additional_data is not None:
        if recall['remedy_id'] is not None:
            query = ('SELECT '
                     'id, '
                     'date, '
                     'description '
                     'from recall_remedies '
                     'WHERE id = %s '
                     'ORDER BY id ASC'
                     )
            cursor.execute(query, [recall['remedy_id']])
            for record in cursor:
                recall['remedy'] = {
                    'id': record['id'],
                    'date': arcimoto.db.datetime_record_output(record['date']),
                    'description': record['description'],
                }

        recall['vehicles'] = []
        query = ('SELECT '
                 'id, '
                 'recall_id, '
                 'service_date, '
                 'service_reference, '
                 'vin '
                 'FROM vehicle_recalls '
                 'WHERE recall_id = %s '
                 'ORDER BY id ASC')
        cursor.execute(query, [recall['recall_id']])
        for record in cursor:
            recall['vehicles'].append({
                'id': record['id'],
                'recall_id': record['recall_id'],
                'service_date': arcimoto.db.datetime_record_output(record['service_date']),
                'service_reference': record['service_reference'],
                'vin': record['vin']
            })

    return recall


lambda_handler = recall_get
