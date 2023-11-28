"""
Purpose:
    This lambda function is meant to be used as an "activity" in an IoT Analytics Pipeline.
Inputs:
    event: a list of telemetry messages from IoT Core
Outputs:
    Returns a list of flattened json messages, so that the VIN is on the same level as the rest of the data
"""
import logging
logger = logging.getLogger("unpack_telemetry_message")
logger.setLevel(logging.DEBUG)


def unpack_telemetry_message(event):
    result = []

    for message in event:
        result_message = {}
        vin = message.get("vin", None)
        logger.info("VIN: {}".format(vin))
        result_message["vin"] = vin
        data = message.get("data", [{}])[0]
        for telemetry_point in data:
            result_message[telemetry_point] = data[telemetry_point]
        result.append(result_message)

    return(result)


def lambda_handler(event, context):

    return unpack_telemetry_message(event)
