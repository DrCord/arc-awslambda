import arcimoto.db


class Authorities:

    def authority_exists(self, id):
        return arcimoto.db.check_record_exists('authority_keys', {'authority_keys_id': id})

    def authority_has_authority_for_vin(self, id, vin):
        return arcimoto.db.check_record_exists('vehicle_authority', {'authority_id': id, 'vin': vin})

    def vehicle_exists(self, vin):
        return arcimoto.db.check_record_exists('vehicle_authority', {'authority_id': 1, 'vin': vin})
