# Architecture Diagram

Serverless, event-driven pipeline. Two independent triggers: an **S3 event**
(push) for ingestion and an **EventBridge schedule** (pull) for reminders. The two
phases are decoupled and only share state through DynamoDB.

```mermaid
flowchart TB
    Aruba([Aruba XML Invoice]) --> S3

    subgraph Ingestion["Ingestion (push, event-driven)"]
        S3[(Amazon S3<br/>raw XML storage)]
        S3 -->|S3 Event Notification<br/>ObjectCreated| ParserLambda
        ParserLambda[AWS Lambda<br/>XML Parser]
    end

    subgraph Storage["Metadata storage"]
        ParserLambda -->|PutItem| Ddb[(Amazon DynamoDB<br/>invoice metadata)]
    end

    subgraph Reminder["Reminder (pull, scheduled)"]
        EB[Amazon EventBridge<br/>scheduled rule]
        EB -->|periodic trigger| ReporterLambda
        ReporterLambda[AWS Lambda<br/>Reminder Reporter]
        ReporterLambda -->|query due dates| Ddb
        ReporterLambda -->|SendEmail| SES[(Amazon SES<br/>email reminder)]
    end

    subgraph Ops["Observability & security"]
        CW[Amazon CloudWatch<br/>Logs]
        IAM[AWS IAM<br/>least privilege]
    end
    ParserLambda -.logs.-> CW
    ReporterLambda -.logs.-> CW
    ParserLambda -.permissions.-> IAM
    ReporterLambda -.permissions.-> IAM

    classDef aws fill:#ff9900,stroke:#232f3e,color:#232f3e,font-weight:bold;
    classDef store fill:#146eb4,stroke:#232f3e,color:#fff;
    class S3,ParserLambda,EB,ReporterLambda,SES,CW,IAM aws;
    class Ddb store;
```

## Proposed evolution (future improvements)

Adding **SQS between S3 and Lambda** introduces a buffer that absorbs upload
spikes and decouples producer from consumer; a **Dead Letter Queue** captures
messages that fail parsing instead of losing them. CloudWatch alarms on Lambda
errors surface failures early.

```mermaid
flowchart LR
    S3[(S3)] -->|event| SQS[Amazon SQS<br/>buffer / decoupling]
    SQS --> Lambda[Lambda parser]
    SQS -.failed messages.-> DLQ[Dead Letter Queue]
    Lambda --> Ddb[(DynamoDB)]
    Lambda -.errors.-> Alarm[CloudWatch Alarm]

    classDef aws fill:#ff9900,stroke:#232f3e,color:#232f3e,font-weight:bold;
    classDef store fill:#146eb4,stroke:#232f3e,color:#fff;
    class Lambda,SQS,DLQ,Alarm aws;
    class S3,Ddb store;
```

## Text fallback

For environments that do not render Mermaid:

```text
Aruba XML Files
        ↓
Amazon S3
        ↓ (ObjectCreated trigger)
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
```
