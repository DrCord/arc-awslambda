# VPCPeering

- [VPCPeering](#vpcpeering)
  - [Description](#description)
  - [Notes](#notes)
  - [Resources](#resources)
  - [Instructions (Individual Stacks)](#instructions-individual-stacks)
  - [Instructions (Nested Stacks)](#instructions-nested-stacks)
  - [Creating more VPC peering connections from different AWS accounts with same accepter account](#creating-more-vpc-peering-connections-from-different-aws-accounts-with-same-accepter-account)

## Description

This solution lets you peer with another VPC in the same or different AWS account. After creating VPC peering connection, additional templates can be deployed to:

- Apply a `Name` tag for the VPC peering connection in the accepter account using a python CloudFormation custom resource.
- Update specified Route Tables & Security Groups
- Supports a comma-delimited list with validation for below parameters:
  - AWS accounts authorized for VPC peering connections
  - Route Tables, to be updated to allow communications via VPC peering connection.

## Notes

- CloudWatch Logs Log Group uses Amazon managed server-side encryption. Optionally, a KMS CMK can be used.
- Amazon S3 Buckets using Amazon managed server-side encryption. Optionally, a KMS CMK can be used.
- **NOTE** Security Group rules are configured to allow all inbound communications from the `VPC Peer CIDR`, this is used as an **EXAMPLE**, however,
  all security group rules can be locked down based on the requirements.
- **NOTE** Route Table routes are configured to allow all inbound communications from the `VPC Peer CIDR`, this is used as an **EXAMPLE**, however,
  all security group rules can be locked down based on the requirements.

## Resources

- [What is VPC Peering?](https://docs.aws.amazon.com/vpc/latest/peering/what-is-vpc-peering.html)
- [VPC Peering Basics](https://docs.aws.amazon.com/vpc/latest/peering/vpc-peering-basics.html)
- [Walkthrough: Peer with an Amazon VPC in another AWS account](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/peer-with-vpc-in-another-account.html)

## Instructions

1. Launch the AWS CloudFormation stack using the `VPCPeering-Accepter-Role.cfn.yaml` template file as the
   source, to create the assumable role in the accepter account that will be used by the requester account. **Note:** If VPC peering connection being
   done between 2 VPCs in the same AWS account, then this step can be skipped.
2. Launch the AWS CloudFormation stack using the `VPCPeering-Requester-Setup.cfn.yaml` template file as
   the source, to create the VPC peering connection in the requester account.
3. Launch the AWS CloudFormation stack using the `VPCPeering-Accepter-Tag.cfn.yaml` template file as the
   source, to apply a name tag on the VPC peering connection in the accepter account.
4. Launch the AWS CloudFormation stack using the `VPCPeering-Updates.cfn.yaml` template file as the source, to update the specified route tables & security groups for communications with the VPC peering connection in the requester account.
5. Launch the AWS CloudFormation stack using the `VPCPeering-Updates.cfn.yaml` template file as the source, to update the specified route tables & security groups for communications with the VPC peering connection in the accepter account.
6. Add DNS private name resolution to the accepter side of the peering connection (this is not supported via cloudformation!) must be done manually via the API at the command line or in the console.

example:

```aws-cli
aws ec2 modify-vpc-peering-connection-options --vpc-peering-connection-id "pcx-036ae317d4fa73b7c" --requester-peering-connection-options '{"AllowDnsResolutionFromRemoteVpc":false}' --accepter-peering-connection-options '{"AllowDnsResolutionFromRemoteVpc":true}' --region us-west-2
```

## Creating more VPC peering connections from different AWS accounts with same accepter account

1. Launch the AWS CloudFormation stack using the [VPCPeering-Accepter-Role.cfn.yaml](templates/VPCPeering-Accepter-Role.cfn.yaml) template file as the source, with the AWS account of the additional requester accounts you will be creating VPC peering connections with.
2. Continue with Step 2 from the [Instructions](#instructions) section.

### Original Source

[aws labs - cloudformation templates](https://github.com/awslabs/aws-cloudformation-templates/blob/master/aws/solutions/VPCPeering/)
