# Y-Risk

[State machine](https://us-west-2.console.aws.amazon.com/states/home?region=us-west-2#/statemachines/view/arn:aws:states:us-west-2:511596272857:stateMachine:Y-Risk-Monthly-Vehicle-Telemetry) to export vehicles telemetry monthly to s3 bucket. Thiis is triggered by a [CloudWatch Event](https://us-west-2.console.aws.amazon.com/cloudwatch/home?region=us-west-2#rules:name=Y-Risk-Monthly-Data-Export)

## State Machine

[State machine](https://us-west-2.console.aws.amazon.com/states/home?region=us-west-2#/statemachines/view/arn:aws:states:us-west-2:511596272857:stateMachine:Y-Risk-Monthly-Vehicle-Telemetry)

### Example Payloads

arcimoto bucket

    {
      "input": {
        "env": "prod",
        "s3_bucket": "arcimoto-yrisk"
      }
    }

y-risk bucket

    {
      "input": {
        "env": "prod",
        "s3_bucket": "y-risk-client-exposure-data"
      }
    }

## CloudWatch Event

[CloudWatch Event](https://us-west-2.console.aws.amazon.com/cloudwatch/home?region=us-west-2#rules:name=Y-Risk-Monthly-Data-Export)

### Example Payload

    {
      "input": {
        "env": "prod",
        "output_yrisk_s3_bucket": true
      }
    }
