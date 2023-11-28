#!/bin/bash

declare -r retention="90"

for L in $(aws logs describe-log-groups \
    --query 'logGroups[?!not_null(retentionInDays)] | [].logGroupName' \
    --output text)
do
  echo "${L}: setting log group retention"
   MSYS_NO_PATHCONV=1 aws logs put-retention-policy --log-group-name ${L} \
   --retention-in-days ${retention}
  echo "${L} cloudwatch log retention updated to ${retention} days"
done