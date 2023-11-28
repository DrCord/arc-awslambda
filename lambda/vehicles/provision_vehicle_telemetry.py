import logging

from arcimoto.exceptions import *
import arcimoto.args
import arcimoto.db
import arcimoto.note
import arcimoto.runtime
import arcimoto.user
import arcimoto.vehicle

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

arcimoto.args.register({
    'vin': {
        'type': 'string',
        'required': True
    },
    'model_release_id': {
        'type': 'integer',
        'required': True,
        'min': 1
    }
})


@arcimoto.runtime.handler
@arcimoto.user.require('vehicles.vehicle.provision')
@arcimoto.db.transaction
def provision_vehicle_telemetry(vin, model_release_id):
    global logger

    vehicle_instance = arcimoto.vehicle.Vehicle(vin)

    vehicle_instance.create(model_release_id)

    msg = f'Vehicle Provisioned with VIN {vin} and model release id {model_release_id}'
    arcimoto.note.ManufacturingNotification(
        message=msg,
        source='provision_vehicle_telemetry',
        data={},
        severity='INFO'
    )
    arcimoto.note.ServiceNotification(
        message=msg,
        source='provision_vehicle_telemetry',
        data={},
        severity='INFO'
    )

    return {}


lambda_handler = provision_vehicle_telemetry
