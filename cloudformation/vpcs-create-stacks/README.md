# Create Stacks: VPCs, DBs, Peering and Endpoints

The AWS API cloudformation commands to `create-stack` and corresponding stacks in the sub-folders of this folder are from a [best practices guide](https://aws.amazon.com/blogs/database/deploy-an-amazon-aurora-postgresql-db-cluster-with-recommended-best-practices-using-aws-cloudformation/) with our customizations. It has a detailed explanation and diagram of what this creates before our customizations.

The bucket `arcimoto-cloudformation`, in the `vpc` folder, contains a copy of the cloudformation templates used in these commands.

## Endpoints

### Timestream

The AWS Console was used to manually create the `timestream` `ingest` and `query` endpoints for our VPCs. The `Telemetry` VPC has both `ingest` and `query` endpoints. The `REEF` and `YRisk` VPCs both have only a `query` endpoint.
