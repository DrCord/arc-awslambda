import logging
import json

from arcimoto.exceptions import *
import arcimoto.runtime
import arcimoto.user
import arcimoto.db

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


@arcimoto.runtime.handler
@arcimoto.user.require('users.abilities.read')
def users_permissions_abilities_list():
    global logger

    # all abilities in system with associated permissions
    user_abilities_object = arcimoto.user.Abilities()
    system_abilities = user_abilities_object.get_abilities()

    return system_abilities


lambda_handler = users_permissions_abilities_list
