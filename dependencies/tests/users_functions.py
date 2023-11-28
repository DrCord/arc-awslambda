import logging
import boto3

from arcimoto.exceptions import *
import arcimoto.runtime

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


def add_permission_to_group(args, test_runner_user_admin=True):
    return arcimoto.runtime.test_invoke_lambda('users_add_permission_to_group', args, test_runner_user_admin)


def remove_permission_from_group(args, test_runner_user_admin=True):
    return arcimoto.runtime.test_invoke_lambda('users_remove_permission_from_group', args, test_runner_user_admin)


def add_preference_to_user(args, test_runner_user_admin=True):
    return arcimoto.runtime.test_invoke_lambda('users_add_preference_to_user', args, test_runner_user_admin)


def add_user_to_group(args, test_runner_user_admin=True):
    return arcimoto.runtime.test_invoke_lambda('users_add_user_to_group', args, test_runner_user_admin)


def remove_user_from_group(args, test_runner_user_admin=True):
    return arcimoto.runtime.test_invoke_lambda('users_remove_user_from_group', args, test_runner_user_admin)


def group_create(args=None, test_runner_user_admin=True):
    if args is None:
        args = {
            'name': 'Unit Test Users'
        }
    response = arcimoto.runtime.test_invoke_lambda('users_group_create', args, test_runner_user_admin)
    return response.get('id', None)


def group_delete(group_id, test_runner_user_admin=True):
    return arcimoto.runtime.test_invoke_lambda('users_group_delete', {'group': group_id}, test_runner_user_admin)


def group_get(group_id, test_runner_user_admin=True):
    return arcimoto.runtime.test_invoke_lambda('users_group_get', {'group': group_id}, test_runner_user_admin)


def user_create(args, test_runner_user_admin=True):
    return arcimoto.runtime.test_invoke_lambda('users_create_user', args, test_runner_user_admin)


def user_disable(username, test_runner_user_admin=True):
    return arcimoto.runtime.test_invoke_lambda('users_disable_user', {'username': username}, test_runner_user_admin)


def user_enable(username, test_runner_user_admin=True):
    return arcimoto.runtime.test_invoke_lambda('users_enable_user', {'username': username}, test_runner_user_admin)


def user_resend_invite(username, test_runner_user_admin=True):
    return arcimoto.runtime.test_invoke_lambda('users_resend_user_invite', {'username': username}, test_runner_user_admin)


def profile_get(username, test_runner_user_admin=True):
    return arcimoto.runtime.test_invoke_lambda('users_profile_get', {'username': username}, test_runner_user_admin)


def profile_update(args, test_runner_user_admin=True):
    return arcimoto.runtime.test_invoke_lambda('users_profile_update', args, test_runner_user_admin)


def user_get(username, test_runner_user_admin=True):
    return arcimoto.runtime.test_invoke_lambda('users_user_get', {'username': username}, test_runner_user_admin)


def user_delete(username, test_runner_user_admin=True):
    return arcimoto.runtime.test_invoke_lambda('users_delete_user', {'username': username}, test_runner_user_admin)


def users_list(args, test_runner_user_admin=True):
    return arcimoto.runtime.test_invoke_lambda('users_users_list', args, test_runner_user_admin)


def groups_list(test_runner_user_admin=True):
    return arcimoto.runtime.test_invoke_lambda('users_groups_list', {}, test_runner_user_admin)


def permissions_abilities_list(test_runner_user_admin=True):
    return arcimoto.runtime.test_invoke_lambda('users_permissions_abilities_list', {}, test_runner_user_admin)


def permissions_ability_create(ability=None, constant=None, description=None, permissions=None, test_runner_user_admin=True):
    return arcimoto.runtime.test_invoke_lambda('users_permissions_ability_create', {'ability': ability, 'constant': constant, 'description': description, 'permissions': permissions}, test_runner_user_admin)


@arcimoto.db.transaction
def permissions_ability_delete(id, test_runner_user_admin=True):
    return arcimoto.runtime.test_invoke_lambda('users_permissions_ability_delete', {'id': id}, test_runner_user_admin)


def permissions_ability_edit(id=None, ability=None, constant=None, description=None, permissions=None, test_runner_user_admin=True):
    return arcimoto.runtime.test_invoke_lambda('users_permissions_ability_edit', {'id': id, 'ability': ability, 'constant': constant, 'description': description, 'permissions': permissions}, test_runner_user_admin)


def permissions_ability_get(id=None, test_runner_user_admin=True):
    return arcimoto.runtime.test_invoke_lambda('users_permissions_ability_get', {'id': id}, test_runner_user_admin)


def permissions_list(args, test_runner_user_admin=True):
    return arcimoto.runtime.test_invoke_lambda('users_permissions_list', args, test_runner_user_admin)


def preferences_list(test_runner_user_admin=True):
    return arcimoto.runtime.test_invoke_lambda('users_preferences_list', {}, test_runner_user_admin)


def ability_grant(username=None, ability_id=None, test_runner_user_admin=True):
    return arcimoto.runtime.test_invoke_lambda('users_ability_grant', {'username': username, 'ability_id': ability_id}, test_runner_user_admin)


def user_mfa_sms_disable(username=None, test_runner_user_admin=True):
    return arcimoto.runtime.test_invoke_lambda('users_user_mfa_sms_disable', {'username': username}, test_runner_user_admin)


def user_mfa_sms_enable(username=None, test_runner_user_admin=True):
    return arcimoto.runtime.test_invoke_lambda('users_user_mfa_sms_enable', {'username': username}, test_runner_user_admin)


def user_mfa_totp_associate_token(access_token=None, test_runner_user_admin=True):
    return arcimoto.runtime.test_invoke_lambda('users_user_mfa_totp_associate_token', {'access_token': access_token}, test_runner_user_admin)


def user_mfa_totp_disable(username=None, test_runner_user_admin=True):
    return arcimoto.runtime.test_invoke_lambda('users_user_mfa_totp_disable', {'username': username}, test_runner_user_admin)


def user_mfa_totp_enable(username=None, test_runner_user_admin=True):
    return arcimoto.runtime.test_invoke_lambda('users_user_mfa_totp_enable', {'username': username}, test_runner_user_admin)


def user_mfa_totp_verify_token(access_token=None, user_code=None, friendly_device_name=None, test_runner_user_admin=True):
    params = {
        'access_token': access_token,
        'user_code': user_code,
        'friendly_device_name': friendly_device_name
    }
    return arcimoto.runtime.test_invoke_lambda('users_user_mfa_totp_verify_token', params, test_runner_user_admin)
