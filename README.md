AWS Aruba Invoice Reminder System
Overview

Serverless AWS pipeline that processes Aruba electronic invoice XML files, extracts payment and due-date information, stores structured data in DynamoDB, and automatically sends reminder emails before invoice expiration.

The project is designed to be:

fully serverless
event-driven
low-cost / AWS Free Tier friendly
scalable and modular
Architecture
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
AWS Services Used
Service	Purpose
Amazon S3	Raw XML storage
AWS Lambda	XML parsing and reporting logic
Amazon DynamoDB	Invoice metadata storage
Amazon EventBridge	Scheduled automation
Amazon SES	Email notification system
Amazon CloudWatch	Logging and monitoring
AWS IAM	Permissions and security
Features
XML invoice ingestion
Automated event-driven processing
Invoice data extraction
Due-date monitoring
Automatic email reminders
Serverless architecture
Cost-optimized AWS design
CloudWatch logging and debugging
Extracted Invoice Data

The pipeline extracts and stores:

Supplier name
Invoice number
Invoice date
Due date
Total amount
Payment amount
Payment status
S3 source path
Project Structure
aws-aruba-invoice-reminder-system/
│
├── lambda/
│   ├── parser/
│   └── reporting/
│
├── architecture/
│
├── sample_data/
│
├── policies/
│
├── docs/
│
└── README.md
Example Workflow
XML invoice uploaded to S3
S3 triggers Lambda automatically
Lambda parses XML invoice
Structured data stored in DynamoDB
EventBridge runs scheduled reporting Lambda
SES sends email reminder report
