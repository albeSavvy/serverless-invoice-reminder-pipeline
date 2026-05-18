# Reporting Lambda

## Purpose

The reporting Lambda is triggered by an EventBridge scheduled rule.

## Responsibilities

- scan or query DynamoDB for upcoming invoice due dates
- identify invoices requiring reminders
- generate an email summary
- send reminder notification through Amazon SES
- log execution results to CloudWatch

## Future Improvements

- avoid full table scans by using a due-date index
- add reminder status tracking
- add retry handling
- add structured report format
