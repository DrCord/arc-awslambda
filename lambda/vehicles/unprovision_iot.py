import boto3
from botocore.exceptions import ClientError
import logging

from arcimoto.exceptions import *
import arcimoto.runtime
import arcimoto.args
import arcimoto.user

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

arcimoto.args.register({
    'vin': {
        'type': 'string',
        'required': True
    }
})


@arcimoto.runtime.handler
@arcimoto.user.require('vehicles.vehicle.provision')
def unprovision_iot(vin):
    global logger, boto3

    iot = boto3.client('iot')

    # Ordering is important. We must tear down connections and associations before we can delete

    # start by looking up the principal (if any)
    list_thing_principals_response = None
    try:
        list_thing_principals_response = iot.list_thing_principals(
            thingName=vin
        )

    except iot.exceptions.ResourceNotFoundException as e:
        # the thing doesn't exist, so we don't have anything to clean up or unprovision
        logger.warn('Thing {} does not exist'.format(vin))
        return {}  # this is a soft-error, since technically we now have an unprovisioned thing

    except ClientError as e:
        raise Exception(e.response['Error']['Message'])

    except Exception as e:
        raise ArcimotoException(e)

    try:
        # loop over any attached principals
        for certificate_arn in list_thing_principals_response['principals']:

            # detach the certificate from the thing
            iot.detach_thing_principal(
                thingName=vin,
                principal=certificate_arn
            )
            logger.info('Detached certificate {} from thing'.format(certificate_arn))

            certificate_id = certificate_arn.split('/')[-1]

            # disable the certificate
            iot.update_certificate(
                certificateId=certificate_id,
                newStatus='INACTIVE'
            )

            # then finally delete it

            iot.delete_certificate(
                certificateId=certificate_id
            )
            logger.info('Deleted certificate')

        iot.delete_thing(
            thingName=vin,
            expectedVersion=1
        )
        logger.info('Deleted thing {}'.format(vin))
    except ClientError as e:
        logger.exception(e.response['Error']['Message'])
        raise Exception(e.response['Error']['Message'])

    return {}


lambda_handler = unprovision_iot
