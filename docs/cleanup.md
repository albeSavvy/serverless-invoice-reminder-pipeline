# Cleanup Guide

To avoid unexpected AWS costs, remove all resources created for the lab when they are no longer needed.

## Resources to Delete

- S3 bucket and uploaded XML files
- Lambda parser function
- Lambda reporting function
- DynamoDB invoice metadata table
- EventBridge scheduled rule
- SES test configuration if no longer needed
- IAM roles and policies created for the project
- CloudWatch log groups

## Suggested Cleanup Order

1. Disable EventBridge scheduled rule.
2. Remove S3 event notifications.
3. Delete Lambda functions.
4. Delete DynamoDB table.
5. Empty and delete S3 bucket.
6. Delete IAM roles and policies.
7. Delete CloudWatch log groups.
8. Review AWS Billing dashboard.

## Cost Safety Checklist

- Check AWS Billing dashboard
- Check AWS Budgets
- Check active Lambda functions
- Check S3 buckets
- Check DynamoDB tables
- Check EventBridge rules
- Check CloudWatch log groups
