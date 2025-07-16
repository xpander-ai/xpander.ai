# Creating a Read-Only IAM User for EKS Access

This tutorial provides a step-by-step guide to create an IAM user with read-only access to an EKS cluster. It uses AWS EKS Access Entries and Kubernetes RBAC to ensure the user can view cluster resources without modification rights.

## Prerequisites
- AWS CLI installed and configured with admin credentials
- kubectl installed
- Access to an EKS cluster
- Basic understanding of IAM and Kubernetes RBAC

## Part 1: Admin Tasks (Using Admin Credentials)
*Note: All commands in this section should be run using your admin AWS credentials*

### Step 1: Create the IAM User
```bash
# Using admin credentials
aws iam create-user --user-name k8s-readonly-user
```

### Step 2: Create an IAM Policy
```bash
# Using admin credentials
aws iam create-policy \
  --policy-name k8s-readonly-policy \
  --policy-document '{
    "Version": "2012-10-17",
    "Statement": [
      {
        "Effect": "Allow",
        "Action": [
          "eks:DescribeCluster",
          "eks:ListClusters",
          "cloudformation:DescribeStacks",
          "cloudwatch:GetMetricData",
          "logs:StartQuery",
          "logs:GetQueryResults",
          "iam:GetRole",
          "iam:GetRolePolicy",
          "iam:ListRolePolicies",
          "iam:ListAttachedRolePolicies",
          "iam:GetPolicy",
          "iam:GetPolicyVersion",
          "eks-mcpserver:QueryKnowledgeBase"
        ],
        "Resource": "*"
      }
    ]
  }'
```

### Step 3: Attach the Policy to the IAM User
```bash
# Using admin credentials
aws iam attach-user-policy \
  --user-name k8s-readonly-user \
  --policy-arn arn:aws:iam::<YOUR_ACCOUNT_ID>:policy/k8s-readonly-policy
```

### Step 4: Create EKS Access Entry
```bash
# Using admin credentials
aws eks create-access-entry \
  --cluster-name <YOUR_CLUSTER_NAME> \
  --region <YOUR_REGION> \
  --principal-arn arn:aws:iam::<YOUR_ACCOUNT_ID>:user/k8s-readonly-user \
  --type STANDARD \
  --kubernetes-groups view
```

### Step 5: Create ClusterRoleBinding
```bash
# Using admin credentials
kubectl create clusterrolebinding view-group-readonly \
  --clusterrole=view \
  --group view
```

### Step 6: Create Access Keys for the IAM User
```bash
# Using admin credentials
aws iam create-access-key --user-name k8s-readonly-user
```
Save the AccessKeyId and SecretAccessKey securely.

## Part 2: Read-Only User Setup (Using Read-Only User Credentials)
*Note: Switch to using the read-only user's credentials for all remaining steps*

### Step 7: Configure AWS CLI Profile for the IAM User
```bash
# Using read-only user credentials
aws configure set aws_access_key_id <ACCESS_KEY_ID> --profile k8s-readonly-user
aws configure set aws_secret_access_key <SECRET_ACCESS_KEY> --profile k8s-readonly-user
aws configure set region <YOUR_REGION> --profile k8s-readonly-user
```

# Part 3: Verification Steps (Optional)

### Step 8 : Update kubeconfig for EKS
```bash
# Using read-only user credentials
aws eks update-kubeconfig \
  --name <YOUR_CLUSTER_NAME> \
  --region <YOUR_REGION> \
  --profile k8s-readonly-user \
  --alias readonly
```

### Step 9: Set the Context
```bash
# Using read-only user credentials
kubectl config use-context readonly
```

### Step 10: Verify Access
```bash
# Using read-only user credentials
kubectl get pods
```

## Important Notes:
1. **Admin Credentials Required for Part 1:**
   - All steps in Part 1 must be performed using admin credentials
   - These steps set up the infrastructure and permissions

2. **Read-Only Credentials for Part 2:**
   - All steps in Part 2 use the read-only user's credentials
   - These steps verify the setup and configure the user's environment

3. **Placeholder Values:**
   Replace all placeholders with your actual values:
   - `<YOUR_ACCOUNT_ID>`
   - `<YOUR_REGION>`
   - `<YOUR_CLUSTER_NAME>`
   - `<ACCESS_KEY_ID>`
   - `<SECRET_ACCESS_KEY>`

4. **Context Management:**
   - The context is named 'readonly' for easy identification
   - You can switch between contexts using `kubectl config use-context <context-name>`
   - To see all available contexts: `kubectl config get-contexts`
   - To see current context: `kubectl config current-context`

## Troubleshooting
- **Access Denied Errors:**
  - Verify you're using the correct credentials for each part
  - Check that all admin steps (Part 1) completed successfully
  - Ensure you're using the correct AWS profile for kubectl commands

- **EKS Access Issues:**
  - If you can't create the Access Entry, ensure you're using admin credentials
  - If you can't create the ClusterRoleBinding, ensure you're using admin credentials
  - If you can't access the cluster, verify the EKS Access Entry and ClusterRoleBinding exist

- **Profile Issues:**
  - If kubectl commands fail, verify you're using the correct AWS profile
  - You can check your current AWS profile with: `aws configure list`

- **Context Issues:**
  - If kubectl commands fail, verify you're using the correct context
  - You can check your current context with: `kubectl config current-context`
  - To switch back to admin context: `kubectl config use-context <admin-context-name>`

## Security Best Practices
1. **Access Key Management:**
   - Store access keys securely
   - Rotate access keys regularly
   - Never commit access keys to version control

2. **Permission Scope:**
   - Follow the principle of least privilege
   - Regularly audit IAM permissions
   - Remove unused access entries

3. **Monitoring:**
   - Enable CloudTrail logging
   - Monitor EKS audit logs
   - Set up alerts for suspicious activities

## Cleanup
To remove the read-only user and associated resources:

```bash
# Using admin credentials
# 1. Delete the EKS access entry
aws eks delete-access-entry \
  --cluster-name <YOUR_CLUSTER_NAME> \
  --region <YOUR_REGION> \
  --principal-arn arn:aws:iam::<YOUR_ACCOUNT_ID>:user/k8s-readonly-user

# 2. Delete the ClusterRoleBinding
kubectl delete clusterrolebinding view-group-readonly

# 3. Detach the policy from the user
aws iam detach-user-policy \
  --user-name k8s-readonly-user \
  --policy-arn arn:aws:iam::<YOUR_ACCOUNT_ID>:policy/k8s-readonly-policy

# 4. Delete the policy
aws iam delete-policy \
  --policy-arn arn:aws:iam::<YOUR_ACCOUNT_ID>:policy/k8s-readonly-policy

# 5. Delete the IAM user
aws iam delete-user --user-name k8s-readonly-user
``` 