Aruba XML Files
        ↓
Amazon S3
        ↓ (trigger)
AWS Lambda - XML Parser
        ↓
Amazon DynamoDB
        ↓ (scheduled execution)
Amazon EventBridge
        ↓
AWS Lambda - Reporting
        ↓
Amazon SES
        ↓
Email Reminder Report
