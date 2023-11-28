# Orders Lamdas

## Concept
The orders lambdas are a mechanism for transporting order reservations and associated payment information to CX and ERP systems

## Email
SQS Enqueued order requests are sent to email resources defined in AWS secrets using SES
- SES
-- See [orders_order_ses_email](./orders_order_ses_email.py])
-- [Html and JSON SES Templates](../utility/ses/templates)
-- [SES README](../utility/ses/templates.README.md)

## ERP Systems

- TBD
