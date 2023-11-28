import logging
import boto3
import json
from datetime import datetime, timedelta

from arcimoto.exceptions import *
import arcimoto.note
import arcimoto.runtime

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

event_bridge_client = None


@arcimoto.runtime.handler
def replicate_events_cleanup():
    global event_bridge_client

    event_bridge_client = boto3.client('events')

    rule_names = list_rule_names_by_target()

    rules_data = []
    rules_deleted = False

    for rule_name in rule_names:
        rule_data = {
            'rule_name': rule_name
        }
        rule_name_parts = rule_name.split('-')
        rule_date = rule_name_parts[-2]

        # parse rule names for older than 2 days to get list of rule to remove
        rule_old = rule_date_check(rule_date)
        rule_data['rule_old'] = rule_old

        # get targets and then remove targets and rule for old rules
        if rule_old:
            rule_remove_targets(rule_name)
            rule_delete(rule_name)
            rules_deleted = True

        rule_data['rule_deleted'] = rule_old

        rules_data.append(rule_data)

    if rules_deleted:
        msg_lines = [
            'Replicate - Events Cleanup',
            'Removed Used DB Retire Deletion Events'
        ]
        msg = '\n'.join(msg_lines)
        if len(rules_data) is not None:
            msg += f'\n\n' + json.dumps(rules_data)

        arcimoto.note.ReplicateNotification(
            message=msg,
            source='replicate_events_cleanup',
            source_type='lambda',
            severity='INFO'
        )

    return {
        'rules_data': rules_data
    }


def list_rule_names_by_target():
    global event_bridge_client

    # list_rule_names_by_target
    target_arn = 'arn:aws:states:us-west-2:511596272857:stateMachine:Replicate-DB-Remove-Retired'
    response = event_bridge_client.list_rule_names_by_target(
        TargetArn=target_arn,
        Limit=100
    )

    return response.get('RuleNames', [])


def rule_date_check(rule_date):
    rule_datetime = datetime.strptime(rule_date, "%Y%m%d")
    two_days_ago = datetime.utcnow() - timedelta(days=2)

    return rule_datetime.date() < two_days_ago.date()


def rule_remove_targets(rule_name):
    global event_bridge_client

    target_ids = list_target_ids_by_rule(rule_name)

    event_bridge_client.remove_targets(
        Rule=rule_name,
        Ids=target_ids,
        Force=True
    )


def list_target_ids_by_rule(rule_name):
    global event_bridge_client

    response = event_bridge_client.list_targets_by_rule(
        Rule=rule_name
    )
    targets = response.get('Targets', [])

    target_ids = []
    for target in targets:
        target_id = target.get('Id', None)
        if target_id is not None:
            target_ids.append(target_id)

    return target_ids


def rule_delete(rule_name):
    global event_bridge_client

    event_bridge_client.delete_rule(
        Name=rule_name,
        Force=True
    )


lambda_handler = replicate_events_cleanup
