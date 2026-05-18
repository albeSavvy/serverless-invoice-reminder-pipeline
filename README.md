# AWS Serverless Invoice Reminder Pipeline

## Overview

This project implements a serverless AWS pipeline for processing Aruba electronic invoice XML files, extracting relevant payment and due-date information, storing structured invoice metadata in Amazon DynamoDB, and sending automated reminder emails before invoice expiration.

The project was designed as a hands-on AWS Data Engineering and Solution Architecture exercise, with a focus on event-driven architecture, serverless services, cost optimization, monitoring, and security best practices.

## Business Scenario

Companies often receive electronic invoices in XML format and need a reliable way to track payment deadlines, monitor invoice status, and notify operators before due dates expire.

This project simulates a real-world workflow where invoice files are uploaded to Amazon S3 and automatically processed by AWS Lambda. Extracted metadata is stored in DynamoDB and later used by a scheduled reporting process to send reminder emails through Amazon SES.

This use case is relevant for operations, finance, procurement, administration, and logistics environments.

## Architecture

The solution follows an event-driven serverless architecture.

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
Scheduled Rule
        |
        v
AWS Lambda
Reminder Reporter
        |
        v
Amazon SES
Email Reminder
