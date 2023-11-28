# Configuring API Gateway

## Stage Variables

Set the function name to a stage variable so a deployed API calls the correct environment lambda automatically:

```text
Lambda Function: ${stageVariables.func_<name_of_lambda>}
```

In the stage variable configuration, define the variable to point to the appropriate version of the lambda:

```text
func_<name_of_lambda> = <name_of_lambda>:<env>
```

## Invocation Permission

In order to execute the appropriate lambda through stage variables, access must be granted to API Gateway. This can only be done through the CLI, and should be set using the [lambda utility](../utility/lambda/README.md) to ensure accuracy and to avoid errors:


```text
$ /python3 ./utility/lambda grant_api --help
usage: lambda grant_api [-h] -a API_ID -p REQUEST_PATH [-e {dev,staging,prod}]
                        function

positional arguments:
  function              the name of the lambda function to allow

optional arguments:
  -h, --help            show this help message and exit
  -a API_ID, --api-id API_ID
                        the ID of the API to allow (default: None)
  -p REQUEST_PATH, --request-path REQUEST_PATH
                        the request method and path to allow (default: None)
  -e {dev,staging,prod}, --env {dev,staging,prod}
                        environment to use (default: dev)
```
