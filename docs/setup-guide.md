# Setup Guide

## Prerequisites

- AWS account
- IAM user or role with required permissions
- Verified Amazon SES email identity
- Basic knowledge of S3, Lambda, DynamoDB, EventBridge, and IAM

## High-Level Setup

1. Create an S3 bucket for XML invoice ingestion.
2. Create a DynamoDB table for invoice metadata.
3. Create the XML parser Lambda function.
4. Configure S3 event notification to trigger Lambda.
5. Create the reporting Lambda function.
6. Configure an EventBridge scheduled rule.
7. Configure Amazon SES for email reminders.
8. Validate logs in CloudWatch.

## Suggested Naming Convention

Use a consistent naming convention:

```text
dev-aruba-invoice-s3-raw
dev-aruba-invoice-lambda-parser
dev-aruba-invoice-lambda-reporter
dev-aruba-invoice-ddb-metadata
dev-aruba-invoice-eventbridge-reminder
dev-aruba-invoice-ses-reminder
```

## Suggested Tags

| Key | Value |
|---|---|
| Project | aruba-invoice-reminder |
| Environment | dev |
| Owner | alberto-savino |
| Purpose | aws-learning |
| CostCenter | personal-lab |
