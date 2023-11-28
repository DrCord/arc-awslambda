# SES Templates

## Template Creation

- Build valid HTML and text files (see template locations section).
  - Use mustache.js commands for templating values from your data_dictionary
    see [AWS Documentation](https://docs.aws.amazon.com/ses/latest/dg/send-personalized-email-advanced.html)
- Use the [arcimoto-ses-utility](https://bitbucket.org/arcimotocode1/arcimoto-ses-utility) `template_upsert` command, passing arguments for the template name and corresponding html and text file locations

## Testing URLs

- [configurator dev](https://dev.d3jflkpwl8j7t6.amplifyapp.com/fuv): [`https://dev.d3jflkpwl8j7t6.amplifyapp.com/fuv`]
- [configurator staging](https://staging.d3jflkpwl8j7t6.amplifyapp.com/fuv): [`https://staging.d3jflkpwl8j7t6.amplifyapp.com/fuv`]

## Template Locations

- HTML amd Text files are stored in [./html/](./html/) and [.text/](./text/) respectively.
- Edit and save files here to pass as arguments to the [arcimoto-ses-utility](https://bitbucket.org/arcimotocode1/arcimoto-ses-utility) `template_upsert` command.

## Examples

### Example structure of a lambda function to send templated email via SES

In the lambda make the following api call via boto3:

```python
ses_client = boto3.client('ses', region_name=AWS_REGION)
response = ses_client.send_templated_email(
    Destination={
        'ToAddresses': [
            recipients
        ]
    },
    Source=SENDER,
    ReplyToAddresses=[SENDER],
    Template=template_name,
    TemplateData=json.dumps(data_dictionary),
    SourceArn=arcimoto.runtime.arn_sections_join('ses', 'valid_email_identity'),
    ReturnPathArn=arcimoto.runtime.arn_sections_join('ses', 'valid_email_identity')
)
```

Where:

- recipents is a single email string or list of emails
- SENDER is is a verified AWS SES email address
- template_name is the unique template name uploaded to SES
- data_dictionary is a python dictionary (may be mutli dimensional)
- valid_email_identity (example: identity/no-reply@arcimoto.com)

### Arcimoto SES Utility Examples

- executed at the `ses/templates/` file path:

    ```cli
    python -m arcimoto_ses_utility template_upsert TEL_orders_order_success_customer_dev --content-file-path-html html/TEL_orders_order_success_customer.html --content-file-path-text text/TEL_orders_order_success_customer.txt
    ```

### Manually creating template file for AWS CLI use

To manually create the JSON file to use at the CLI use a JSON escape utility to transform your HTML to a string
    see [freeformatter.com](https://www.freeformatter.com/json-escape.html) or an equivalent utility
    {
        "Template": {
        "TemplateName": "NAME OF YOUR TEMPLATE",
        "SubjectPart": "SUBJECT",
        "HtmlPart": "JSON ESCAPED HTML",
        "TextPart": "JSON ESCAPED TEXT"
        }
    }

## Pipeline

The SES Templates `TEL_orders_order_success_customer_{{ENV}}` and `TEL_orders_order_success_CX_{{ENV}}` used in the configurator order process are maintained automatically by the awslambda repo pipeline from the source files `TEL_orders_order_success_customer.[html|txt]` and `TEL_orders_order_success_CX.[html|txt]` respectively. If the pipeline detects changes to either the html or text files that are the source for the template it rebuilds and updates the SES Template in AWS.

Related pipeline steps in `bitbucket-pipelines.yml`:

- ses-update-template-orders-success-customer-dev
- ses-update-template-orders-success-customer-staging
- ses-update-template-orders-success-customer-prod

- ses-update-template-orders-success-cx-dev
- ses-update-template-orders-success-cx-staging
- ses-update-template-orders-success-cx-prod
