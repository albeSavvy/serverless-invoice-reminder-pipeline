# Cost Optimization

## Strategy

This project is designed to minimize costs by using serverless and pay-per-use AWS services.

## Cost-Friendly Choices

| Component | Cost Optimization Choice |
|---|---|
| Compute | AWS Lambda instead of EC2 |
| Storage | Amazon S3 for low-cost object storage |
| Database | DynamoDB with low usage or on-demand mode |
| Scheduling | EventBridge scheduled rule |
| Email | SES for low-cost notification |
| Monitoring | CloudWatch with retention control |

## Main Cost Risks

| Risk | Mitigation |
|---|---|
| Excessive test uploads | Clean S3 test files regularly |
| Recursive S3 triggers | Separate input and output prefixes |
| CloudWatch logs growth | Set log retention to 7 or 14 days |
| DynamoDB growth | Delete test records when no longer needed |
| SES sending volume | Use verified test recipients |

## Recommended Controls

- Configure AWS Budgets
- Monitor Lambda invocations
- Set CloudWatch log retention
- Use S3 lifecycle policies
- Review DynamoDB table usage
- Clean up unused resources after testing

## Expected Demo Cost

For a small personal lab workload, the expected cost should remain very low and potentially within the AWS Free Tier, depending on account eligibility and usage volume.
