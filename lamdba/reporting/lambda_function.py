import boto3
from datetime import datetime, timedelta
from decimal import Decimal

dynamodb = boto3.resource("dynamodb")
ses = boto3.client("ses")

TABLE_NAME = "ArubaInvoices"

# Replace with your verified SES email
SENDER_EMAIL = "your_verified_email@example.com"
RECIPIENT_EMAIL = "your_verified_email@example.com"

table = dynamodb.Table(TABLE_NAME)


def format_euro(value):
    """
    Formats Decimal values into European currency format.
    Example:
    6062.6 -> € 6.062,60
    """
    if value is None:
        return "€ 0,00"

    value = Decimal(str(value))

    return (
        f"€ {value:,.2f}"
        .replace(",", "X")
        .replace(".", ",")
        .replace("X", ".")
    )


def lambda_handler(event, context):

    today = datetime.utcnow().date()
    limit_date = today + timedelta(days=2)

    response = table.scan()
    items = response.get("Items", [])

    due_soon = []
    future_due = []

    for item in items:

        due_date_str = item.get("due_date")

        if not due_date_str:
            continue

        due_date = datetime.strptime(
            due_date_str,
            "%Y-%m-%d"
        ).date()

        if (
            today <= due_date <= limit_date
            and item.get("payment_status") == "unpaid"
        ):
            due_soon.append(item)

        elif (
            due_date > limit_date
            and item.get("payment_status") == "unpaid"
        ):
            future_due.append(item)

    due_soon.sort(
        key=lambda x: x.get("due_date", "")
    )

    future_due.sort(
        key=lambda x: x.get("due_date", "")
    )

    lines = []

    lines.append("AWS INVOICE REMINDER REPORT")
    lines.append("")
    lines.append(f"Today: {today}")
    lines.append(f"Due date threshold: {limit_date}")
    lines.append("")

    lines.append("INVOICES DUE WITHIN 2 DAYS")
    lines.append("-----------------------------------")

    if due_soon:

        for item in due_soon:

            lines.append(
                f"- {item.get('supplier_name')} | "
                f"Due: {item.get('due_date')} | "
                f"Amount: {format_euro(item.get('payment_amount'))} | "
                f"Invoice: {item.get('invoice_number')}"
            )

    else:

        lines.append(
            "No invoices due within the next 2 days."
        )

    lines.append("")
    lines.append("UPCOMING FUTURE DUE DATES")
    lines.append("-----------------------------------")

    if future_due:

        for item in future_due:

            lines.append(
                f"- {item.get('supplier_name')} | "
                f"Due: {item.get('due_date')} | "
                f"Amount: {format_euro(item.get('payment_amount'))} | "
                f"Invoice: {item.get('invoice_number')}"
            )

    else:

        lines.append(
            "No future unpaid invoices found."
        )

    email_body = "\n".join(lines)

    ses.send_email(
        Source=SENDER_EMAIL,
        Destination={
            "ToAddresses": [
                RECIPIENT_EMAIL
            ]
        },
        Message={
            "Subject": {
                "Data": "Invoice Due Reminder Report",
                "Charset": "UTF-8"
            },
            "Body": {
                "Text": {
                    "Data": email_body,
                    "Charset": "UTF-8"
                }
            }
        }
    )

    print(email_body)

    return {
        "statusCode": 200,
        "message": "Report sent successfully",
        "due_soon_count": len(due_soon),
        "future_due_count": len(future_due)
    }
