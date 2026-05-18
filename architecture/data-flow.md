# Data Flow

## End-to-End Flow

```text
1. XML invoice uploaded to S3
2. S3 event triggers parser Lambda
3. Parser Lambda reads XML content
4. Invoice metadata is extracted
5. Metadata is stored in DynamoDB
6. EventBridge triggers reporting Lambda on schedule
7. Reporting Lambda checks due dates
8. SES sends reminder email
9. CloudWatch stores logs
```

## Logical Layers

| Layer | AWS Service | Responsibility |
|---|---|---|
| Ingestion | Amazon S3 | Receive raw XML files |
| Processing | AWS Lambda | Parse and validate invoice data |
| Storage | Amazon DynamoDB | Store structured metadata |
| Orchestration | Amazon EventBridge | Schedule reminder execution |
| Notification | Amazon SES | Send email reminders |
| Observability | Amazon CloudWatch | Log and monitor execution |

## Data Engineering Notes

The project separates raw ingestion from structured metadata storage.

This supports:

- better traceability
- easier reprocessing
- improved debugging
- future analytics extensions
