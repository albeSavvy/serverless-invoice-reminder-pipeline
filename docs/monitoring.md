# Monitoring

## Monitoring Goals

The monitoring layer should help answer:

- Did the XML file trigger the parser Lambda?
- Did the parser complete successfully?
- Was invoice metadata stored in DynamoDB?
- Did EventBridge run the scheduled reporting process?
- Was the reminder email sent through SES?
- Were any errors generated?

## CloudWatch Logs

Each Lambda function should write meaningful logs to CloudWatch.

Recommended log events:

- file received
- parsing started
- parsing completed
- validation errors
- DynamoDB write result
- reminder check started
- email sent
- execution failed

## Recommended Metrics

| Component | Metric |
|---|---|
| Lambda | Invocations |
| Lambda | Errors |
| Lambda | Duration |
| Lambda | Throttles |
| DynamoDB | Read/Write capacity |
| EventBridge | Trigger execution |
| SES | Email sending activity |

## Future Improvements

- CloudWatch Alarm on Lambda errors
- Dead Letter Queue for failed events
- Structured JSON logging
- Dashboard for operational visibility
