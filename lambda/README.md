# Lambda Functions

This folder contains the planned AWS Lambda functions for the project.

## Functions

| Function | Purpose |
|---|---|
| parser | Parses uploaded Aruba XML invoice files |
| reporting | Checks invoice due dates and sends reminder emails |

## Runtime

Suggested runtime:

```text
Python 3.12
```

## Configuration

Recommended environment variables:

```text
DYNAMODB_TABLE_NAME
SES_SENDER_EMAIL
SES_RECIPIENT_EMAIL
LOG_LEVEL
```

## Best Practices

- Keep functions small and focused
- Avoid hardcoded configuration
- Use environment variables
- Add structured logging
- Handle parsing errors gracefully
- Validate XML input before storing data
