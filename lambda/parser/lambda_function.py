import json
import logging
import os
import xml.etree.ElementTree as ET
from datetime import datetime

import boto3

logger = logging.getLogger()
logger.setLevel(logging.INFO)

s3_client = boto3.client("s3")
dynamodb = boto3.resource("dynamodb")

table_name = os.environ.get("DYNAMODB_TABLE_NAME", "invoice-metadata")
table = dynamodb.Table(table_name)


def extract_text(root, tag_name):
    element = root.find(f".//{tag_name}")
    return element.text.strip() if element is not None and element.text else None


def lambda_handler(event, context):
    logger.info("Parser Lambda started")
    logger.info(json.dumps(event))

    try:
        for record in event["Records"]:
            bucket_name = record["s3"]["bucket"]["name"]
            object_key = record["s3"]["object"]["key"]

            logger.info(f"Processing file: s3://{bucket_name}/{object_key}")

            response = s3_client.get_object(
                Bucket=bucket_name,
                Key=object_key
            )

            xml_content = response["Body"].read()
            root = ET.fromstring(xml_content)

            invoice_data = {
                "invoice_number": extract_text(root, "Numero"),
                "supplier_name": extract_text(root, "Denominazione"),
                "invoice_date": extract_text(root, "Data"),
                "due_date": extract_text(root, "DataScadenzaPagamento"),
                "total_amount": extract_text(root, "ImportoTotaleDocumento"),
                "payment_amount": extract_text(root, "ImportoPagamento"),
                "payment_status": "PENDING",
                "s3_source_path": f"s3://{bucket_name}/{object_key}",
                "processed_timestamp": datetime.utcnow().isoformat()
            }

            logger.info(f"Extracted invoice data: {invoice_data}")

            table.put_item(Item=invoice_data)

            logger.info("Invoice metadata successfully stored in DynamoDB")

        return {
            "statusCode": 200,
            "body": json.dumps("Invoice successfully processed")
        }

    except Exception as error:
        logger.exception("Error processing invoice")

        return {
            "statusCode": 500,
            "body": json.dumps(str(error))
        }
