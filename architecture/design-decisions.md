# Design Decisions

This document explains *why* each service was chosen, which alternatives were
considered, and the trade-off accepted. The guiding question is not "which AWS
service do I add?" but "which problem am I solving and which trade-off do I
accept?".

## Serverless First

The project uses a serverless architecture to reduce operational overhead and
avoid paying for idle infrastructure. The workload is sporadic (a few invoices a
day) and bursty, so always-on compute would be wasted cost.

## Event-Driven Ingestion

S3 event notifications trigger processing only when a new XML invoice is uploaded.
Nothing polls S3 in a loop: the event itself drives the work.

## Two Decoupled Triggers: Event (ingestion) + Schedule (reminder)

The pipeline has **two independent rhythms**, and this is the core architectural
point:

1. **Ingestion (push):** an invoice lands in S3 -> `ObjectCreated` wakes the
   parser Lambda -> metadata is written to DynamoDB.
2. **Reminder (pull):** EventBridge, on a schedule, wakes the reporter Lambda ->
   it queries DynamoDB for upcoming due dates -> SES sends the email.

The two phases are **decoupled**: ingestion knows nothing about reminders and vice
versa. They communicate only through shared state in DynamoDB. Trade-off accepted:
two Lambdas and a shared state to keep consistent, in exchange for being able to
change the reminder logic without touching ingestion.

## DynamoDB for Metadata

DynamoDB stores structured invoice metadata because the access patterns are few
and known in advance.

Example access patterns:

- retrieve invoice by invoice number
- list invoices by due date
- identify upcoming due dates
- identify overdue invoices

### Why not a relational database (RDS / Aurora)?

- **Problem:** store flat invoice records (supplier, number, dates, amounts,
  status) and query them by due date.
- **Alternative considered:** RDS / Aurora relational engine.
- **Choice:** DynamoDB, one record per invoice, key-based access.
- **Trade-off accepted:** no rich relational queries (joins, ad-hoc reports) in
  exchange for zero idle cost and automatic scaling.

The reasoning in one paragraph: the access patterns are few and known, there are
no joins and no ad-hoc queries. With a sporadic, event-driven load, an always-on
relational engine like RDS would mean wasted idle cost and connection pooling to
manage from Lambda (Lambdas scale, DB connections do not, which pushes you toward
RDS Proxy and extra complexity). DynamoDB gives pay-per-request, scales to zero at
rest, and millisecond latency. The price paid is rigidity: indexes must be
designed around the access patterns up front, and free-form analytics are offloaded
to Athena / QuickSight on exported data (see future improvements).

## Scheduled Reminder Logic

EventBridge runs reminder checks on a schedule without requiring a server-based
cron job. Trade-off: one more managed service to learn, in exchange for no machine
kept running just to fire a timer.

## Email Notification

Amazon SES sends email reminders because it integrates well with AWS and supports
low-cost notification workflows. Trade-off: identities/domains must be verified to
leave the SES sandbox, in exchange for very low cost and managed deliverability.

## Main Tradeoffs

| Decision | Benefit | Tradeoff |
|---|---|---|
| Lambda | Low cost and scalable | Not ideal for long-running jobs |
| S3 trigger | Simple event-driven ingestion | Requires careful trigger configuration |
| DynamoDB | Serverless and scalable | Requires access pattern planning; no joins |
| EventBridge | Managed scheduling, no cron server | One more service to learn |
| SES | Low-cost email service | Requires verified identities in sandbox |
| Manual setup | Good for learning | Less repeatable than IaC |

## Future Architecture Improvements

- Add Infrastructure as Code (AWS CDK in Python is the natural candidate)
- Add SQS between S3 and Lambda for decoupling and buffering
- Add a Dead Letter Queue for failed processing
- Add CloudWatch Alarms on Lambda errors
- Add Step Functions for complex workflows
- Add Glue and Athena / QuickSight for analytics on invoice metadata
