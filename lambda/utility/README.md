# Resource Bundle: Utility

Miscellaneous functions, including devops and maintenance and other support functions.

## message_broker

General purpose message handling system. Accepts messages from multiple sources and routes to appropriate destinations based on severity and source.

## print_label_request

Trigger a label print request through Odoo

## slack_notification

Sample message:

    {
        "AlarmName": "EC2 - memory percent used - STAGE-InfluxDB",
        "AlarmDescription": "STAGE-InfluxDB EC2 Memory Percent Used outside of 2 sigma band",
        "AWSAccountId": "511596272857",
        "NewStateValue": "ALARM",
        "NewStateReason": "Thresholds Crossed: 2 out of the last 2 datapoints [28.244242980188464 (22/11/19 00:57:00), 27.035814838199848 (22/11/19 00:52:00)] were less than the lower thresholds [31.723549397187316, 31.317673764600034] or greater than the upper thresholds [33.09242087209403, 32.68864166862828] (minimum 2 datapoints for OK -> ALARM transition).",
        "StateChangeTime": "2019-11-22T01:02:17.570+0000",
        "Region": "US West (Oregon)",
        "OldStateValue": "OK",
        "Trigger": {
            "Period": 300,
            "EvaluationPeriods": 2,
            "ComparisonOperator": "LessThanLowerOrGreaterThanUpperThreshold",
            "ThresholdMetricId": "ad1",
            "TreatMissingData": "- TreatMissingData:                    missing",
            "EvaluateLowSampleCountPercentile": "",
            "Metrics": [
                {
                    "Id": "m1",
                    "MetricStat": {
                        "Metric": {
                            "Dimensions": [
                                {
                                    "value": "i-046d48b26d0fd82ca",
                                    "name": "InstanceId"
                                },
                                {
                                    "value": "ami-04b762b4289fba92b",
                                    "name": "ImageId"
                                },
                                {
                                    "value": "t2.micro",
                                    "name": "InstanceType"
                                }
                            ],
                            "MetricName": "mem_used_percent",
                            "Namespace": "CWAgent"
                        },
                        "Period": 300,
                        "Stat": "Average"
                    },
                    "ReturnData": true
                },
                {
                    "Expression": "ANOMALY_DETECTION_BAND(m1, 0.2)",
                    "Id": "ad1",
                    "Label": "mem_used_percent (expected)",
                    "ReturnData": true
                }
            ]
        }
    }

## step_wrapper

Multi-step execution tool with in-built rollback behavior.

### Step Wrapper Rules

- atoms element contains a list of dictionaries with 'labmda' and 'reverse' elements

- an error in any 'lambda' function will halt execution and call the 'reverse' for any successful atoms in reverse order

- 'reverse' lambda functions cannot fail

- functions are idempotent
  - calling a function repeatedly is fine (for retries and lost responses)

### Controlled Docs Masterlist Export

A simple utility lambda for automating export of controlled documents masterlist. Uses a google service account to assume a role in the Arcimoto Google Workspace to access masterlist, generate CSVs by department, and upload to S3 bucket.

## Undocumented (possibly deprecated)

- monitor_influx_backup
- set_continuous_queries
