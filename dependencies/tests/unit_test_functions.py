import arcimoto.runtime


def unit_test_bundles_get_lambdas(args):
    return arcimoto.runtime.test_invoke_lambda('unit_test_bundles_get_lambdas', args, False)


def unit_test_lambda_get_tests(args):
    return arcimoto.runtime.test_invoke_lambda('unit_test_lambda_get_tests', args, False)


def unit_test_lambda_run_tests(args):
    return arcimoto.runtime.test_invoke_lambda('unit_test_lambda_run_tests', args, False)


def unit_test_lambdas_tests_report(args):
    return arcimoto.runtime.test_invoke_lambda('unit_test_lambdas_tests_report', args, False)


def unit_test_notify(args):
    return arcimoto.runtime.test_invoke_lambda('unit_test_notify', args, False)
