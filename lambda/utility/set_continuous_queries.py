import json
import requests
import boto3
import rds_auth

import logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


def set_continuous_queries(env, version):
    # This section pulled directly from get_telemetry_definition.py
    client = boto3.client('s3')
    response = None
    if version is None:
        response = client.get_object(
            Bucket='arcimoto-telemetry',
            Key='config/metrics.json'
        )
        logger.warning("No version configured - using latest telemetry definitions")
        version = response.get("VersionId", None)
    else:
        response = client.get_object(
            Bucket='arcimoto-telemetry',
            Key='config/metrics.json',
            VersionId=version
        )
    if response is None:
        raise Exception("Unable to fetch telemetry definitions from S3")

    # insert the version as a top-level element of the returned metric.json
    file_content = response["Body"].read().decode('utf-8')
    file_json = json.loads(file_content)
    file_json['_version'] = version

    # setup for sending CQs to Influx
    # Influx endpoints
    PROD_url = 'http://172.30.0.203:90'
    STAGE_url = 'http://172.30.0.72:90'
    DEV_url = 'http://172.30.0.28:90'
    URLs = {"prod": PROD_url,
            "staging": STAGE_url,
            "dev": DEV_url}
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    # other Influx settings
    telemetry_db_name = "amtelemetry"
    default_RP_name = "30d"
    extended_RP_name = "365d"
    downsample_period = "30m"  # 30 minutes
    # the function names in the ql_functions dictionary should match the "downsample" labels in grafana_telemetry_points.json
    ql_functions = {"avg": "mean",     # returns the average value
                    "nz": "top",       # returns the highest value
                    "latest": "last"}  # returns field value with latest timestamp
    ql_args = {"avg": "",
               "nz": ", 1",
               "latest": ""}

    # send CQs to Influx
    for key in file_json.keys():
        if key[0] != '_':
            report = file_json[key].get("report", "latest")
            logger.debug("{}: {}".format(key, report))
            query_name = "_".join([key, report])+" ON "+telemetry_db_name

            my_query = " BEGIN SELECT "+ql_functions[report]+"("+key+ql_args[report]+") AS "+ql_functions[report]+"_"+key + \
                       " INTO \""+extended_RP_name+"\".\"telemetry\"" + \
                       " FROM \""+default_RP_name+"\".\"telemetry\" GROUP BY time("+downsample_period+"), * END"

            r = requests.post(URLs[env]+"/query", data="q=DROP CONTINUOUS QUERY "+query_name, headers=headers)
            logger.debug(r.content)
            r = requests.post(URLs[env]+"/query", data="q=CREATE CONTINUOUS QUERY "+query_name+my_query, headers=headers)
            logger.debug(r.content)


def lambda_handler(event, context):
    # logger.debug("event: {}".format(event))
    version = event.get('version', None)

    # Get env from ARN
    arn = context.invoked_function_arn
    env = rds_auth.get_env_from_arn(arn)
    logger.debug("env: {}".format(env))

    set_continuous_queries(env, version)
