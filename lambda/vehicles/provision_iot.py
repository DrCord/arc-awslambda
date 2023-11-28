import logging
import boto3
from botocore.exceptions import ClientError
import time

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
def provision_iot(vin, thing_type='default-type', thing_group='production'):
    '''creates the iot thing, generates certificate materials and attaches them to the thing'''
    global logger, boto3

    # enforce prefix
    env = arcimoto.runtime.get_env()

    if env == 'dev':
        if not vin.startswith('DEV-'):
            raise ArcimotoArgumentError('Executing in dev env and VIN has no DEV- prefix')
        thing_group = 'development'
    elif env == 'staging':
        if not vin.startswith('STAGE-'):
            raise ArcimotoArgumentError('Executing in staging env and VIN has no STAGE- prefix')
        thing_group = 'staging'
    elif env == 'prod':
        if vin.startswith('STAGE-'):
            raise ArcimotoArgumentError('Executing in prod env and VIN has STAGE- prefix')
        if vin.startswith('DEV-'):
            raise ArcimotoArgumentError('Executing in prod env and VIN has DEV- prefix')
        thing_group = 'production'

    iot_client = boto3.client('iot')

    thing_arn = None
    certificate_arn = None
    cert_attached = False

    response = {}

    # create the thing, allowing for it to already exist
    thing_arn = None
    try:
        create_thing_response = iot_client.create_thing(
            thingName=vin,
            thingTypeName=thing_type,
            attributePayload={
                'attributes': {
                    'vin': vin,
                    'date_provisioned': str(int(time.time()))
                },
                'merge': True
            }
        )
        thing_arn = create_thing_response['thingArn']
    except iot_client.exceptions.ResourceAlreadyExistsException as e:
        logger.warn('Thing "{}" already exists'.format(vin))

        # if it already exists, fetch the arn for the following the code
        describe_thing_response = iot_client.describe_thing(
            thingName=vin
        )
        thing_arn = describe_thing_response['thingArn']

    except ClientError as e:
        raise ArcimotoException(e.response['Error']['Message'])

    response['thing_arn'] = thing_arn
    logger.info('Created Thing "{}": {}'.format(vin, thing_arn))

    # if the thing isn't in the requested group, add it to the group
    list_thing_groups_response = None
    try:
        list_thing_groups_response = iot_client.list_thing_groups_for_thing(
            thingName=vin
        )
    except ClientError as e:
        raise ArcimotoException(e.response['Error']['Message'])

    need_group = True
    for group in list_thing_groups_response['thingGroups']:
        if group['groupName'] == thing_group:
            need_group = False
            break

    if need_group:
        iot_client.add_thing_to_thing_group(
            thingGroupName=thing_group,
            thingGroupArn=arcimoto.runtime.arn_sections_join('iot', 'thinggroup/{}'.format(thing_group)),
            thingName=vin,
            thingArn=thing_arn
        )

    return response


lambda_handler = provision_iot
