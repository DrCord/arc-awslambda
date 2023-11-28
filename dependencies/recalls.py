import arcimoto.db


class Recalls:

    def recall_exists(self, id):
        return arcimoto.db.check_record_exists('recalls', {'id': id})

    def recall_has_remedy(self, recall_id):
        return arcimoto.db.check_record_exists('recalls', {'id': recall_id}, 'remedy_id')

    def vehicle_in_recall(self, vin, recall_id):
        return arcimoto.db.check_record_exists('vehicle_recalls', {'vin': vin, 'recall_id': recall_id})

    def vehicle_recall_exists(self, vehicle_recall_id, recall_id=None, vin=None):
        if vehicle_recall_id is not None:
            return arcimoto.db.check_record_exists('vehicle_recalls', {'id': vehicle_recall_id})
        else:
            return arcimoto.db.check_record_exists('vehicle_recalls', {'recall_id': recall_id, 'vin': vin})

    def vehicle_exists(self, vin):
        return arcimoto.db.check_record_exists('vehicle', {'vin': vin})
