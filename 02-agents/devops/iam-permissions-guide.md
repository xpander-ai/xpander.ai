# IAM Permissions Guide for DevOps Agent

This guide outlines the AWS IAM permissions required to use the DevOps agent effectively. Configure these permissions based on your security requirements and use cases.

## Quick Setup

### Option 1: Read-Only Access (Recommended for Getting Started)
Create an IAM user with read-only permissions to safely explore AWS resources:

```bash
aws iam create-user --user-name devops-agent-user

aws iam attach-user-policy \
  --user-name devops-agent-user \
  --policy-arn arn:aws:iam::aws:policy/ReadOnlyAccess

aws iam create-access-key --user-name devops-agent-user
```

### Option 2: Custom Policy for Core Features
Create a tailored policy with permissions for the agent's main capabilities:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "EKSReadAccess",
      "Effect": "Allow",
      "Action": [
        "eks:Describe*",
        "eks:List*"
      ],
      "Resource": "*"
    },
    {
      "Sid": "EC2ReadAccess",
      "Effect": "Allow",
      "Action": [
        "ec2:Describe*",
        "ec2:GetConsoleOutput"
      ],
      "Resource": "*"
    },
    {
      "Sid": "CostExplorerAccess",
      "Effect": "Allow",
      "Action": [
        "ce:GetCostAndUsage",
        "ce:GetCostForecast",
        "ce:DescribeCostCategoryDefinition",
        "pricing:GetProducts"
      ],
      "Resource": "*"
    },
    {
      "Sid": "CloudWatchReadAccess",
      "Effect": "Allow",
      "Action": [
        "cloudwatch:GetMetric*",
        "cloudwatch:ListMetrics",
        "logs:FilterLogEvents",
        "logs:GetLogEvents"
      ],
      "Resource": "*"
    },
    {
      "Sid": "IAMReadAccess",
      "Effect": "Allow",
      "Action": [
        "iam:GetRole",
        "iam:GetRolePolicy",
        "iam:ListRolePolicies",
        "iam:ListAttachedRolePolicies"
      ],
      "Resource": "*"
    }
  ]
}
```

## Permission Sets by Feature

### EKS Management
```json
{
  "Action": [
    "eks:DescribeCluster",
    "eks:ListClusters",
    "eks:DescribeNodegroup",
    "eks:ListNodegroups",
    "eks:ListFargateProfiles",
    "eks:DescribeFargateProfile"
  ],
  "Resource": "*",
  "Effect": "Allow"
}
```

### Cost Analysis
```json
{
  "Action": [
    "ce:GetCostAndUsage",
    "ce:GetCostForecast",
    "ce:GetReservationUtilization",
    "ce:GetSavingsPlansPurchaseRecommendation",
    "pricing:GetProducts",
    "pricing:DescribeServices"
  ],
  "Resource": "*",
  "Effect": "Allow"
}
```

### Multi-Region Operations
```json
{
  "Action": [
    "ec2:DescribeRegions",
    "ec2:DescribeAvailabilityZones"
  ],
  "Resource": "*",
  "Effect": "Allow"
}
```

### CloudFormation (for Infrastructure Analysis)
```json
{
  "Action": [
    "cloudformation:DescribeStacks",
    "cloudformation:ListStacks",
    "cloudformation:GetTemplate"
  ],
  "Resource": "*",
  "Effect": "Allow"
}
```

## Setup Instructions

1. **Create IAM User:**
```bash
aws iam create-user --user-name devops-agent-user
```

2. **Create Custom Policy:**
```bash
aws iam create-policy \
  --policy-name devops-agent-policy \
  --policy-document file://policy.json
```

3. **Attach Policy:**
```bash
aws iam attach-user-policy \
  --user-name devops-agent-user \
  --policy-arn arn:aws:iam::<ACCOUNT_ID>:policy/devops-agent-policy
```

4. **Create Access Keys:**
```bash
aws iam create-access-key --user-name devops-agent-user
```

5. **Configure AWS CLI:**
```bash
aws configure --profile devops-agent
# Enter Access Key ID
# Enter Secret Access Key
# Enter Default Region
# Enter Output Format (json)
```

## Security Best Practices

### Principle of Least Privilege
- Start with read-only permissions
- Add write permissions only when needed
- Use resource-specific ARNs when possible

### Access Key Management
- Rotate access keys every 90 days
- Never commit credentials to version control
- Use AWS Secrets Manager for production

### Monitoring
- Enable CloudTrail logging
- Set up CloudWatch alarms for unusual API activity
- Review IAM Access Advisor regularly

### Additional Recommendations
- Use MFA for sensitive operations
- Implement IP address restrictions
- Use temporary credentials with STS when possible
- Tag resources for cost tracking

## Common Use Cases

### Development Environment
Use read-only access with limited EC2 describe permissions.

### Production Monitoring
Add CloudWatch and Cost Explorer permissions for comprehensive monitoring.

### CI/CD Integration
Use temporary credentials from STS with assume role permissions.

## Troubleshooting

**Access Denied Errors:**
- Verify the IAM policy is attached correctly
- Check if resource-level permissions are needed
- Ensure the correct AWS profile is being used

**Region-Specific Issues:**
- Some services require region-specific endpoints
- Verify the service is available in your region

**Cost Explorer Not Working:**
- Cost Explorer must be enabled in the AWS Console first
- Data may take 24 hours to appear after enabling

## Cleanup

Remove the IAM user and associated resources:
```bash
# Detach policies
aws iam detach-user-policy \
  --user-name devops-agent-user \
  --policy-arn <POLICY_ARN>

# Delete access keys
aws iam delete-access-key \
  --user-name devops-agent-user \
  --access-key-id <ACCESS_KEY_ID>

# Delete user
aws iam delete-user --user-name devops-agent-user

# Delete custom policy
aws iam delete-policy --policy-arn <POLICY_ARN>
```