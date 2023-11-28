# API Gateway - Exports/Backups

This folder contains swagger exports/backups of the AWS API Gateway configuration for each API implementation in json format as well as directions to export/import the files.

[APIs](https://us-west-2.console.aws.amazon.com/apigateway/main/apis?region=us-west-2)

- [Authority Manager](https://us-west-2.console.aws.amazon.com/apigateway/home?region=us-west-2#/apis/8xlss9lsy0/resources/6t1u9zstw2)
- [Vehicle Manager](https://us-west-2.console.aws.amazon.com/apigateway/home?region=us-west-2#/apis/dsbyqxkezg/resources/goknu5wxgh)

## Prerequisites

In order to use the CLI, you will also need the proper AWS credentials, managed by the AWS [Identity and Access Management (IAM)](https://console.aws.amazon.com/iam/home?#/home) service.  Have the Arcimoto AWS administrator create CLI credentials for you, or give you IAM permission to create them yourself.  Then on the command line run:

```bash
aws configure
```

and enter the Access Key ID and Secret Access Key that you just created.

## Export

To create a new backup when changes are made to an API endpoint export the API and save it here in version control. [How to export original source info](https://docs.aws.amazon.com/en_pv/apigateway/latest/developerguide/api-gateway-export-api.html)

Use the export_apis.py file in the utility directory, see below for information about usage.

### Command parmeters

api_names

- authorityManager
- palantir - this is no longer tracked here, the [Palantir-API cloudformation template](https://us-west-2.console.aws.amazon.com/cloudformation/home?region=us-west-2#/stacks/stackinfo?filteringStatus=active&filteringText=Palantir&viewNested=true&hideStacks=false&stackId=arn%3Aaws%3Acloudformation%3Aus-west-2%3A511596272857%3Astack%2FPalantir-API%2F361739d0-e4fe-11eb-b113-0a9b91f626e1) from the Palantir repo is the source of truth
- recallsPublic
- reef
- statistics
- userManager
- vehicleManager
- web

stage_names

- dev
- staging
- prod

### Example command

```bash
python ./utility/export_apis.py --api_names vehicleManager palantir --stage_names dev staging prod
```

## Import

There are [instructions for importing](https://docs.aws.amazon.com/apigateway/latest/developerguide/api-gateway-import-api.html) in the AWS documentation.
