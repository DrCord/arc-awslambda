# Create Stacks: VPC Bastion hosts

The AWS API cloudformation commands to `create-stack` and corresponding stack in this folder are from a [best practices guide](https://aws.amazon.com/blogs/database/deploy-an-amazon-aurora-postgresql-db-cluster-with-recommended-best-practices-using-aws-cloudformation/) with our customizations. It has a detailed explanation and diagram of what this creates before our customizations.

The bucket `arcimoto-cloudformation`, in the `vpc` folder, contains a copy of the cloudformation template used in this command.

## NOTES

- The IP address to allow access to the bastion host via SSH in the commands is set to the developers personal IP, which is not a long term solution - long-term it should be the network IP that we can VPN into that then allows us access to these resources, so the bastion hosts aren't available to the internet in general.
