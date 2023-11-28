import logging
import json

from arcimoto.exceptions import *
import arcimoto.args
import arcimoto.runtime

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

arcimoto.args.register({
    'bundles': {
        'type': 'list',
        'default': []  # empty list signifies to get all bundles
    }
})


@arcimoto.runtime.handler
def unit_test_bundles_get_lambdas(bundles):
    global logger

    dependencies = dependencies_load()

    lambdas_config = dependencies.get('functions', None)
    if lambdas_config is None:
        raise ArcimotoAlertException('Unable to get lambda config from dependencies')

    lambda_bundles = bucket_lambdas_bundles(lambdas_config)
    bundles_to_fetch = None
    lambdas_bundled = []

    get_all_bundles = len(bundles) == 0
    if get_all_bundles:
        bundles_to_fetch = []
        for bundle_name in lambda_bundles.keys():
            if 'tests' not in bundle_name:
                bundles_to_fetch.append(bundle_name)
    else:
        bundles_to_fetch = bundles

    for bundle_name, bundle_lambdas in {key: value for key, value in sorted(lambda_bundles.items())}.items():
        if 'tests' not in bundle_name:
            for input_bundle in bundles_to_fetch:
                if input_bundle == bundle_name:
                    lambdas_bundled.append({
                        'bundle_name': bundle_name,
                        'lambdas': bundle_lambdas
                    })
                    continue

    lambdas_test_or_non = bucket_lambdas_tests_or_non(lambdas_config, bundles_to_fetch)

    lambdas_non_test = lambdas_test_or_non.get('non_test', [])

    return {
        'lambdas_bundled': lambdas_bundled,
        'bundles_fetched': sorted(bundles_to_fetch),
        'fetched_bundles_lambdas_count': len(lambdas_non_test)
    }


def bucket_lambdas_tests_or_non(lambdas_config, bundles):
    bucketed_lambdas = {
        'non_test': [],
        'test': []
    }

    for lambda_name, lambda_config in lambdas_config.items():
        bundle = lambda_config.get('bundle', None)
        if bundle in bundles:
            bucketed_lambdas['non_test'].append(lambda_name)
        elif bundle.replace('/tests', '') in bundles:
            bucketed_lambdas['test'].append(lambda_name)

    return bucketed_lambdas


def bucket_lambdas_bundles(lambdas_config):
    lambda_bundles = {}

    # use lambdas configuration to sort all lambda names into bundle buckets mappings
    for lambda_name, lambda_config in lambdas_config.items():
        bundle = lambda_config.get('bundle', None)
        if bundle is None:
            raise ArcimotoAlertException(f'Unable to get lambda {lambda_name} bundle')
        if bundle not in lambda_bundles:
            lambda_bundles[bundle] = []
        lambda_bundles[bundle].append(lambda_name)

    return lambda_bundles


def dependencies_load():
    # load all lambda dependency config

    f = open('dependencies.json')
    dependencies = json.load(f)
    f.close()

    return dependencies


lambda_handler = unit_test_bundles_get_lambdas
