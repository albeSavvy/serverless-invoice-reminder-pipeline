# AWS Serverless Invoice Reminder Pipeline

## Project in One Sentence

I built a serverless AWS pipeline that processes Aruba XML invoices, extracts payment due-date metadata, stores it in DynamoDB, and sends automated email reminders before invoice expiration.

## What I Built

This project is a small cloud-based invoice monitoring system designed to reduce manual tracking of electronic invoice deadlines.

It includes:

- XML invoice ingestion through Amazon S3
- Lambda-based XML parsing
- DynamoDB metadata storage
- scheduled due-date checks with EventBridge
- automated email reminders through Amazon SES
- CloudWatch logging for troubleshooting

## Why I Built It

I built this project to practice AWS serverless and data engineering concepts in a realistic administrative and operations-oriented scenario.

The goal was to move beyond theoretical study and implement a practical automation workflow that could support invoice monitoring, payment tracking, and operational reminders.

## Architecture at a Glance

```text
Aruba XML Invoice
        |
        v
Amazon S3
Raw XML Storage
        |
        v
S3 Event Notification
        |
        v
AWS Lambda
XML Parser
        |
        v
Amazon DynamoDB
Invoice Metadata
        |
        v
Amazon EventBridge
Scheduled Checks
        |
        v
AWS Lambda
Reminder Reporter
        |
        v
Amazon SES
Email Reminder
```

## AWS Services Used

| Service | Purpose |
|---|---|
| Amazon S3 | Stores raw XML invoice files |
| AWS Lambda | Parses XML files and generates reminder reports |
| Amazon DynamoDB | Stores structured invoice metadata |
| Amazon EventBridge | Runs scheduled reminder checks |
| Amazon SES | Sends reminder emails |
| Amazon CloudWatch | Provides logs and monitoring |
| AWS IAM | Manages permissions and security |

## Extracted Invoice Data

The pipeline is designed to extract and store:

| Field | Description |
|---|---|
| Supplier name | Invoice supplier or vendor |
| Invoice number | Unique invoice identifier |
| Invoice date | Original invoice issue date |
| Due date | Payment expiration date |
| Total amount | Total invoice amount |
| Payment amount | Amount to be paid |
| Payment status | Pending, paid, overdue, or unknown |
| S3 source path | Original XML location in Amazon S3 |

## What I Learned

- How to design an event-driven AWS workflow
- How to use S3 as an ingestion layer
- How Lambda can process files without running servers
- How DynamoDB can store structured metadata
- How EventBridge can schedule recurring checks
- How SES can support automated operational notifications
- How to think about IAM least privilege, monitoring, cleanup, and cost optimization

## Future Improvements

- Add production-ready XML parsing for more invoice formats
- Add SQS between S3 and Lambda for better decoupling
- Add Dead Letter Queue for failed processing
- Add CloudWatch alarms on Lambda errors
- Add Terraform or CloudFormation infrastructure as code
- Add unit tests for XML parsing logic
- Add QuickSight or Athena analytics on invoice metadata

## Technical Documentation

- [Architecture Diagram](architecture/README.md)
- [Data Flow](architecture/data-flow.md)
- [Design Decisions](architecture/design-decisions.md)
- [Project Overview](docs/project-overview.md)
- [Setup Guide](docs/setup-guide.md)
- [Cost Optimization](docs/cost-optimization.md)
- [Security](docs/security.md)
- [Monitoring](docs/monitoring.md)
- [Cleanup](docs/cleanup.md)

## Certification Alignment

This project supports practical learning for AWS Data Engineering and Solution Architecture topics such as S3-based ingestion, Lambda processing, DynamoDB metadata storage, EventBridge scheduling, SES notifications, IAM least privilege, monitoring, and cost optimization.

## Repository Structure

```text
serverless-invoice-reminder-pipeline/
│
├── README.md
├── .gitignore
├── architecture/
├── docs/
├── lambda/
├── sample_data/
└── policies/
```

## Author

Created by Alberto Savino as part of a practical AWS learning path focused on Data Engineering, Process Improvement, and Solution Architecture.
