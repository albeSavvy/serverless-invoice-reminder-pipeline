import json
import boto3
import xml.etree.ElementTree as ET
from decimal import Decimal
from datetime import datetime
from urllib.parse import unquote_plus

s3 = boto3.client("s3")
dynamodb = boto3.resource("dynamodb")

TABLE_NAME = "ArubaInvoices"
table = dynamodb.Table(TABLE_NAME)


def clean_amount(value):
    if value is None:
        return None
    return Decimal(value.replace(",", "."))


def find_text(root, tag_name):
    """
    Finds the first XML tag matching tag_name, ignoring namespaces.
    """
    for elem in root.iter():
        if elem.tag.endswith(tag_name):
            return elem.text
    return None


def lambda_handler(event, context):
    print("Received event:")
    print(json.dumps(event))

    record = event["Records"][0]
    bucket = record["s3"]["bucket"]["name"]
    key = unquote_plus(record["s3"]["object"]["key"])

    print(f"Bucket: {bucket}")
    print(f"S3 key: {key}")

    response = s3.get_object(Bucket=bucket, Key=key)
    xml_content = response["Body"].read()

    root = ET.fromstring(xml_content)

    supplier_name = find_text(root, "Denominazione")
    invoice_number = find_text(root, "Numero")
    invoice_date = find_text(root, "Data")
    due_date = find_text(root, "DataScadenzaPagamento")
    total_amount = clean_amount(find_text(root, "ImportoTotaleDocumento"))
    payment_amount = clean_amount(find_text(root, "ImportoPagamento"))

    item = {
        "invoice_id": key.split("/")[-1],
        "s3_key": key,
        "supplier_name": supplier_name,
        "invoice_number": invoice_number,
        "invoice_date": invoice_date,
        "due_date": due_date,
        "total_amount": total_amount,
        "payment_amount": payment_amount,
        "payment_status": "unpaid",
        "created_at": datetime.utcnow().isoformat()
    }

    table.put_item(Item=item)

    print("Record saved to DynamoDB:")
    print(json.dumps(item, ensure_ascii=False, default=str))

    return {
        "statusCode": 200,
        "body": json.dumps(item, ensure_ascii=False, default=str)
    }
