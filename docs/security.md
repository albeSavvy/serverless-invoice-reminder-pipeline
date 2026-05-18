# Security Considerations

## IAM Least Privilege

Each Lambda function should only receive the permissions required for its specific task.

The parser Lambda should be allowed to:

- read objects from the invoice S3 bucket
- write metadata to the DynamoDB table
- write logs to CloudWatch

The reporting Lambda should be allowed to:

- read invoice metadata from DynamoDB
- send emails through SES
- write logs to CloudWatch

## S3 Security

Recommended settings:

- block public access
- enable server-side encryption
- restrict bucket access through IAM
- avoid storing sensitive production files in a personal lab account

## Secrets and Configuration

Avoid hardcoding:

- email addresses
- table names
- bucket names
- AWS credentials

Use environment variables for runtime configuration.

## Logging

CloudWatch logs should support troubleshooting without exposing sensitive invoice data.

Avoid logging:

- full invoice content
- personal data
- tax identifiers
- payment details
