# Set all cloudwatch log group retention periods

You can run this script to set all the cloudwatch log group retention periods to 90 days. After running it you can go into the AWS Console and manually set any ones that error - sometimes they seem to error with `InvalidParameterException` and say the log group name doen't match the regular expression for the constraint, but looking at the items that error they seem fine... So easier to just fix a few directly after the script and move on...