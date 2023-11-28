#!/bin/bash
# single input argument is security group id, for example `sg-0f5bac9d758d6cba2`
# example call `sh ./sg-find-dependencies.sh sg-0f5bac9d758d6cba2`
# outputs direct dependency network interfaces of the security group

aws ec2 describe-network-interfaces --filters 'Name=group-id,Values='$1 | grep NetworkInterfaceId
