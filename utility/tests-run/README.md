# tests runner script

## Usage

1. Output list of lambdas

    ```aws-cli
    aws lambda list-functions \
      --query \
        'Functions[?starts_with(FunctionName, `test_`) == `false`]|[?starts_with(FunctionName, `CR-TagVpcPeeringConnections`) == `false`]|[?starts_with(FunctionName, `amplify-login-`) == `false`]|[?starts_with(FunctionName, `serverlessrepo-`) == `false`]|[?starts_with(FunctionName, `util_`) == `false`].FunctionName' \
      --output text \
    > functions_dump.txt
    ```

2. Test lambdas and output results `./lambdas_test.sh`
