# Parser Lambda

## Purpose

The parser Lambda is triggered when a new Aruba XML invoice is uploaded to Amazon S3.

## Responsibilities

- read the XML file from S3
- parse invoice fields
- validate required data
- write structured metadata to DynamoDB
- log processing results to CloudWatch

## Expected Input

An Aruba electronic invoice XML file uploaded to the configured S3 bucket.

## Expected Output

A DynamoDB item containing structured invoice metadata.
