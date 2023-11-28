# Create Stacks: VPC

The AWS API cloudformation commands to `create-stack` and corresponding stack in this folder are from a [best practices guide](https://aws.amazon.com/blogs/database/deploy-an-amazon-aurora-postgresql-db-cluster-with-recommended-best-practices-using-aws-cloudformation/) with our customizations. It has a detailed explanation and diagram of what this creates before our customizations.

The bucket `arcimoto-cloudformation`, in the `vpc` folder, contains a copy of the cloudformation template used in this command.

## Customizations

Added a MainLambda security group to the private subnets. This has access to the secrets-manager endpoint.
