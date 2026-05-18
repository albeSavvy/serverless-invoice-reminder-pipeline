import json
import logging
import os
from datetime import datetime, timedelta

import boto3
from boto3.dynamodb.conditions import Attr

logger = logging.getLogger()
logger.setLevel(logging.INFO)

ses_client = boto3.client("ses")
dynamodb = boto3.resource("dynamodb")

table_name = os.environ.get("DYNAMODB_TABLE_NAME", "invoice-metadata")
sender_email = os.environ.get("SES_SENDER_EMAIL")
recipient_email = os.environ.get("SES_RECIPIENT_EMAIL")

invoice_table = dynamodb.Table(table_name)


def lambda_handler(event, context):
    logger.info("Reminder reporting Lambda started")

    try:
        today = datetime.utcnow().date()
        reminder_limit = today + timedelta(days=7)

        logger.info(f"Checking invoices due before: {reminder_limit}")

        response = invoice_table.scan(
            FilterExpression=Attr("payment_status").eq("PENDING")
        )

        items = response.get("Items", [])
        due_invoices = []

        for item in items:
            due_date = item.get("due_date")

            if not due_date:
                continue

            try:
                due_date_object = datetime.strptime(due_date, "%Y-%m-%d").date()

                if due_date_object <= reminder_limit:
                    due_invoices.append(item)

            except ValueError:
                logger.warning(f"Invalid due date format: {due_date}")

        if not due_invoices:
            logger.info("No invoices requiring reminder")

            return {
                "statusCode": 200,
                "body": json.dumps("No reminders required")
            }

        email_body = "Upcoming invoice due dates:\n\n"

        for invoice in due_invoices:
            email_body += (
                f"Supplier: {invoice.get('supplier_name')}\n"
                f"Invoice: {invoice.get('invoice_number')}\n"
                f"Due Date: {invoice.get('due_date')}\n"
                f"Amount: {invoice.get('payment_amount')}\n"
                "-----------------------------\n"
            )

        ses_client.send_email(
            Source=sender_email,
            Destination={
                "ToAddresses": [recipient_email]
            },
            Message={
                "Subject": {
                    "Data": "Invoice Reminder Report"
                },
                "Body": {
                    "Text": {
                        "Data": email_body
                    }
                }
            }
        )

        logger.info("Reminder email successfully sent")

        return {
            "statusCode": 200,
            "body": json.dumps("Reminder report successfully sent")
        }

    except Exception as error:
        logger.exception("Error generating reminder report")

        return {
            "statusCode": 500,
            "body": json.dumps(str(error))
        }
