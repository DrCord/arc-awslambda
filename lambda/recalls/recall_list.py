import logging

from arcimoto.exceptions import *
import arcimoto.runtime
import arcimoto.user
import arcimoto.db

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

arcimoto.args.register({
    'get_deleted_recalls': {
        'type': 'boolean',
        'nullable': True,
        'default': False
    }
})


@arcimoto.runtime.handler
@arcimoto.user.require('recalls.recall.read')
def recall_list(get_deleted_recalls):
    global logger

    cursor = arcimoto.db.get_cursor()
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
             )

    if get_deleted_recalls is None or not get_deleted_recalls:
        query += 'WHERE status != \'deleted\' '

    query += 'ORDER BY id ASC'
    cursor.execute(query)

    recalls = []
    for record in cursor:
        recalls.append(
            {
                'recall_id': record['id'],
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
        )

    return {'recalls': recalls}


lambda_handler = recall_list
