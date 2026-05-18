# IAM Policies

This folder is intended to contain example IAM policies for the project.

## Policy Goals

Policies should follow the principle of least privilege.

## Planned Policies

| Policy | Purpose |
|---|---|
| lambda-parser-policy.json | Allow parser Lambda to read S3 and write to DynamoDB |
| lambda-reporting-policy.json | Allow reporting Lambda to read DynamoDB and send SES emails |
| cloudwatch-logging-policy.json | Allow Lambda functions to write logs |

## Security Notes

Avoid broad permissions such as:

```text
s3:*
dynamodb:*
ses:*
```

Prefer resource-specific permissions whenever possible.
