import arcimoto.runtime


def controlled_docs_masterlist_export():
    return arcimoto.runtime.test_invoke_lambda('utility_controlled_docs_masterlist_export', {}, False)


def cwl_set_retention():
    return arcimoto.runtime.test_invoke_lambda('utility_cwl_set_retention', {}, False)


def email_alert_error(args, test_runner_user_admin=True):
    return arcimoto.runtime.test_invoke_lambda('utility_email_alert_error', args, test_runner_user_admin)


def print_label(args, test_runner_user_admin=True):
    return arcimoto.runtime.test_invoke_lambda('print_label_request', args, test_runner_user_admin)


def slack_notification(args):
    return arcimoto.runtime.test_invoke_lambda('slack_notification', args, False)


def step_wrapper(args, test_runner_user_admin=True):
    return arcimoto.runtime.test_invoke_lambda('step_wrapper', args, test_runner_user_admin)


def step_wrapper_palantir(args, test_runner_user_admin=True):
    return arcimoto.runtime.test_invoke_lambda('step_wrapper_palantir', args, test_runner_user_admin)
