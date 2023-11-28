import logging
import boto3
import json
import copy

from arcimoto.exceptions import *
import arcimoto.args
import arcimoto.runtime

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


arcimoto.args.register({
    'input': {
        'type': 'dict',
        'required': True,
        'empty': False
    },
    'atoms': {
        'type': 'list',
        'required': True,
        'empty': False
    },
    'params': {
        'type': 'dict',
        'default': {}
    }
})


@arcimoto.runtime.handler
def step_wrapper_palantir(input, atoms, params):
    global logger
    result = {}

    try:
        # make a deep copy of input args so we can mutate without touching input
        args = copy.deepcopy(input)
        # add user's auth token if available to args so lambdas being run can use it
        auth_token = params.get('header', {}).get('Authorization', '')
        if auth_token:
            args['params'] = {
                'header': {
                    'Authorization': auth_token
                }
            }

        # check that the requested atoms are specified correctly
        for atom in atoms:
            if not atom.get('lambda', None):
                raise ArcimotoArgumentError('All atoms must have defined lambda')

        env = arcimoto.runtime.get_env()
        # walk the list of requested atoms, calling in order
        performed_atoms = []
        try:
            for atom in atoms:
                # note that we attempted the step
                performed_atoms.append(atom)
                atom_result = arcimoto.runtime.invoke_lambda(atom.get('lambda'), args)
                # move output to args as appropriate
                output = atom.get('output', None)
                if output and atom_result:
                    for output_name, input_name in output.items():
                        args[input_name] = atom_result[output_name]

            result = copy.deepcopy(args)

        except ArcimotoAlertException as e:
            _unroll_atoms(reversed(performed_atoms), args)
            raise ArcimotoAlertException(e) from e
        except ArcimotoArgumentError as e:
            # argument validation failed,
            # the lambda never really ran and so should not be reversed,
            # remove it from the list
            del performed_atoms[-1]
            if len(performed_atoms):
                _unroll_atoms(reversed(performed_atoms), args)
            raise ArcimotoArgumentError(e) from e
        except ArcimotoHighAlertException as e:
            _unroll_atoms(reversed(performed_atoms), args)
            raise ArcimotoHighAlertException(e) from e
        except ArcimotoNoStepUnrollException as e:
            raise ArcimotoNoStepUnrollException(e) from e
        except ArcimotoNotFoundError as e:
            _unroll_atoms(reversed(performed_atoms), args)
            raise ArcimotoNotFoundError(e) from e
        except ArcimotoPermissionError as e:
            # user permission validation failed,
            # the lambda never really ran and so should not be reversed,
            # remove it from the list
            del performed_atoms[-1]
            if len(performed_atoms):
                _unroll_atoms(reversed(performed_atoms), args)
            raise ArcimotoPermissionError(e) from e
        except Exception as e:
            _unroll_atoms(reversed(performed_atoms), args)
            raise ArcimotoException(e) from e

    except Exception as e:
        raise e

    # remove user token data from returned result
    if auth_token:
        del result['params']

    return result


def _unroll_atoms(atoms, args):
    global logger

    for atom in atoms:
        logger.info(f'===== Attempting to unroll atom {atom.get("lambda")} =====')
        lambda_reverse_name = atom.get('reverse', None)
        if lambda_reverse_name:
            arcimoto.runtime.invoke_lambda(lambda_reverse_name, args)


lambda_handler = step_wrapper_palantir
