#!/bin/bash
# single input argument is vpc id, for example `vpc-0da94cd96c671ebf4`
# example call `sh ./vpc-find-dependencies.sh vpc-0da94cd96c671ebf4`
# outputs direct dependencies of the VPC those dependencies may have further dependencies

aws ec2 describe-internet-gateways --filters 'Name=attachment.vpc-id,Values='$1 | grep InternetGatewayId
aws ec2 describe-subnets --filters 'Name=vpc-id,Values='$1 | grep SubnetId
aws ec2 describe-route-tables --filters 'Name=vpc-id,Values='$1 | grep RouteTableId
aws ec2 describe-network-acls --filters 'Name=vpc-id,Values='$1 | grep NetworkAclId
aws ec2 describe-vpc-peering-connections --filters 'Name=requester-vpc-info.vpc-id,Values='$1 | grep VpcPeeringConnectionId
aws ec2 describe-vpc-endpoints --filters 'Name=vpc-id,Values='$1 | grep VpcEndpointId
aws ec2 describe-nat-gateways --filter 'Name=vpc-id,Values='$1 | grep NatGatewayId
aws ec2 describe-security-groups --filters 'Name=vpc-id,Values='$1 | grep GroupId
aws ec2 describe-instances --filters 'Name=vpc-id,Values='$1 | grep InstanceId
aws ec2 describe-vpn-gateways --filters 'Name=attachment.vpc-id,Values='$1 | grep VpnGatewayId
aws ec2 describe-network-interfaces --filters 'Name=vpc-id,Values='$1 | grep NetworkInterfaceId
