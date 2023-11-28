import logging
import boto3
import datetime
import json

from arcimoto.exceptions import *
import arcimoto.args
import arcimoto.runtime

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

arcimoto.args.register({
    'replication_target_env': {
        'type': 'string',
        'required': True,
        'allowed': [
            'dev',
            'staging'
        ]
    },
    'db_type': {
        'type': 'string',
        'required': True,
        'allowed': [
            'authkey',
            'main'
        ]
    },
    'db_cluster_identifier': {
        'type': 'string',
        'empty': False,
        'nullable': True,
        'default': None,
        'regex': '^.*retired.*$'
    },
    'db_instance_identifier': {
        'type': 'string',
        'required': True,
        'empty': False,
        'regex': '^.*retired.*$'
    }
})


@arcimoto.runtime.handler
def replicate_db_retired_schedule_removal(replication_target_env, db_type, db_cluster_identifier, db_instance_identifier):
    client = boto3.client('events')

    role_arn = 'arn:aws:iam::511596272857:role/replicate.step_functions'

    # datetime object containing current date and time
    now = datetime.datetime.now()
    dt_string_postfix = now.strftime('%Y%m%d-%H%M%S')
    event_name = f'rds-replicate-remove-retired-db-{db_type}-{replication_target_env}-{dt_string_postfix}'

    schedule_expression = cron_expression_generate()

    put_rule_response = client.put_rule(
        Name=event_name,
        RoleArn=role_arn,
        ScheduleExpression=schedule_expression,
        State='ENABLED',
        Description=f'Schedule removal of RDS DB instance and associated cluster retired during replication. db_cluster_identifier: {db_cluster_identifier}, db_instance_identifier: {db_instance_identifier}',
        Tags=[
            {
                'Key': 'Cost Center',
                'Value': 'Telematics'
            }
        ]
    )

    # check returned successfully
    if put_rule_response['ResponseMetadata']['HTTPStatusCode'] == 200:
        logger.info(f'Successfully created event bridge rule for removal of {db_cluster_identifier}/{db_instance_identifier}')
    else:
        raise ArcimotoReplicateAlertException(f'Unable to create event bridge rule for removal of {db_cluster_identifier}/{db_instance_identifier}')

    state_machine_input = {
        'input': {
            'run_env': arcimoto.runtime.get_env(),
            'replication_target_env': replication_target_env,
            'db_cluster_identifier': db_cluster_identifier,
            'db_instance_identifier': db_instance_identifier
        }
    }

    put_targets_response = client.put_targets(
        Rule=event_name,
        Targets=[
            {
                'Id': 'RemoveRetiredDB',
                'Arn': 'arn:aws:states:us-west-2:511596272857:stateMachine:Replicate-DB-Remove-Retired',
                'RoleArn': role_arn,
                'Input': json.dumps(state_machine_input)
            }
        ]
    )

    # check returned successfully
    if put_targets_response['ResponseMetadata']['HTTPStatusCode'] == 200:
        logger.info(f'Successfully added target to event bridge rule for removal of {db_cluster_identifier}/{db_instance_identifier}')
    else:
        raise ArcimotoReplicateAlertException(f'Unable to add target to event bridge rule for removal of {db_cluster_identifier}/{db_instance_identifier}')

    success_message = f'Retired DB removal {event_name} scheduled for {schedule_expression}: db_cluster_identifier: {db_cluster_identifier}, db_instance_identifier: {db_instance_identifier}'

    return {
        'message': success_message
    }


def cron_expression_generate():
    # get tomorrow to schedule 1 day from now
    tomorrow = datetime.datetime.utcnow() + datetime.timedelta(days=1)
    minutes = tomorrow.strftime('%M')
    hours = tomorrow.strftime('%H')
    day_of_month = tomorrow.strftime('%d')
    month = tomorrow.strftime('%m')
    year = tomorrow.strftime('%Y')

    # do not set day of week
    day_of_week = '?'

    # define a single point in time event
    # order of schedule is cron(minutes|hours|day of month|month|day of week|year)
    cron_expressions = [
        minutes,
        hours,
        day_of_month,
        month,
        day_of_week,
        year
    ]
    cron_expression = ' '.join(cron_expressions)
    schedule_expression = f'cron({cron_expression})'

    return schedule_expression


lambda_handler = replicate_db_retired_schedule_removal
