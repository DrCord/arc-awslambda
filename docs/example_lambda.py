# system level imports first
import logging

# arcimoto specific imports
from arcimoto.exceptions import *
import arcimoto.runtime
import arcimoto.args
import arcimoto.user
import arcimoto.db

# configure logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# configure input validation
# NOTE: argument names will be pulled from the lambda event and passed as keyword arguments
# to the main function
arcimoto.args.register({
    'name': {
        'type': 'string',
        'required': True,
        'empty': False
    },
    'id': {
        'type': 'integer',
        'required': True,
        'min': 1
    },
    'additional': {
        'type': 'string',
        'empty': False,
        'required': False,
        'default': 'DEFAULT'
    }
})


# Designate a primary function for the lambda. runtime.handler must be the first decorator
@arcimoto.runtime.handler
# any number of required permissions may be stacked. ArcimotoPermissionError raised on failure
@arcimoto.user.require('users.user.create')
@arcimoto.user.require('users.group.read')
# if you would like automatic rollback/commit behavior
@arcimoto.db.transaction
def main_function(name, id, additional):

    # do some DB work
    cursor = arcimoto.db.get_cursor()
    query = "SELECT column FROM table WHERE column=%s"
    values = [arg_1]
    logger.debug(cursor.mogrify(query, values))
    cursor.execute(query, values)
    element = cursor.fetchone()
    result = element.get('column', None)

    # throwing errors will be caught and handled appropriately based on exception class
    if result is None:
        raise ArcimotoNotFoundError("No matching column found")

    # always return a dictionary
    # NOTE: an empty dictionary will be returned for you if you forget to return or return None
    return {
        "result": "Executed experimental magic with name {}, id {}, additional {}".format(name, id, additional)
    }


# lambda_handler must be set to the main entry point symbol
lambda_handler = main_function
