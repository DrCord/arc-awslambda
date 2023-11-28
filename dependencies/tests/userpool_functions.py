import arcimoto.runtime


def userpool_trigger_custom_message():
    return arcimoto.runtime.test_invoke_lambda('userpool_trigger_custom_message', {}, False)
