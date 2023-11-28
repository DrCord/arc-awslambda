import logging
import boto3
from botocore.exceptions import ClientError

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
def unprovision_iot_certificate(vin):
    global logger, boto3

    iot = boto3.client('iot')

    # see if thing already has a principal
    list_thing_principals_response = None
    try:

        list_thing_principals_response = iot.list_thing_principals(
            thingName=vin
        )

    except iot.exceptions.ResourceNotFoundException as e:
        logger.exception('Thing {} does not exist'.format(vin))
        raise ArcimotoNotFoundError('Invalid VIN')

    except ClientError as e:
        logger.exception('Principal lookup failed')
        raise ArcimotoException(e.response['Error']['Message'])

    try:
        # remove any currently attached principals
        for certificate_arn in list_thing_principals_response['principals']:

            # get a list of all attached policies
            list_policies_response = iot.list_attached_policies(
                target=certificate_arn
            )

            # detach all policies
            for policy in list_policies_response['policies']:
                iot.detach_policy(
                    policyName=policy['policyName'],
                    target=certificate_arn
                )

            # detach the cert first
            iot.detach_thing_principal(
                thingName=vin,
                principal=certificate_arn
            )

            certificate_id = certificate_arn.split('/')[-1]

            # disable the certificate
            iot.update_certificate(
                certificateId=certificate_id,
                newStatus='INACTIVE'
            )

            # and finally delete it
            iot.delete_certificate(
                certificateId=certificate_id
            )
            logger.info('Deleted certificate {} attached to thing {}'.format(
                certificate_arn, vin))

    except ClientError as e:
        logger.exception(e.response['Error']['Message'])
        raise ArcimotoException(e.response['Error']['Message'])

    # return empty on success
    return {}


lambda_handler = unprovision_iot_certificate
