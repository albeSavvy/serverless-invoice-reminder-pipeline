# Design Decisions

## Serverless First

The project uses a serverless architecture to reduce operational overhead and avoid paying for idle infrastructure.

## Event-Driven Ingestion

S3 event notifications are used to trigger processing only when a new XML invoice is uploaded.

## DynamoDB for Metadata

DynamoDB is used to store structured invoice metadata because the access patterns are simple and predictable.

Example access patterns:

- retrieve invoice by invoice number
- list invoices by due date
- identify upcoming due dates
- identify overdue invoices

## Scheduled Reminder Logic

EventBridge is used to run reminder checks on a schedule without requiring a server-based cron job.

## Email Notification

Amazon SES is used for email reminders because it integrates well with AWS and supports low-cost notification workflows.

## Main Tradeoffs

| Decision | Benefit | Tradeoff |
|---|---|---|
| Lambda | Low cost and scalable | Not ideal for long-running jobs |
| S3 trigger | Simple event-driven ingestion | Requires careful trigger configuration |
| DynamoDB | Serverless and scalable | Requires access pattern planning |
| SES | Low-cost email service | Requires verified identities in sandbox |
| Manual setup | Good for learning | Less repeatable than IaC |

## Future Architecture Improvements

- Add Infrastructure as Code
- Add SQS between S3 and Lambda
- Add Dead Letter Queue
- Add CloudWatch Alarms
- Add Step Functions for complex workflows
- Add Glue and Athena for analytics
