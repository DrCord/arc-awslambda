# Resource Bundle: Hologram

Functions related to hologram.io integration.

## how it works

- cloudwatch hourly cron job calls hologram_check_plans
- hologram_check_plans gets all the plans that will expire within the next 24 hours
- then adds those device_id(actually link_id) to the sqs queue `hologram_change_plan_{ENV}`
- messages in the queue trigger the lambda `hologram_change_plan`
- `hologram_change_plan` makes API calls to update the device plans to the hologram API

## NOTE

Warning - Hologram has no environment so all of our lambdas interface with the same environment, prod!!
