# DevOps Agent

A conversational AI agent for AWS infrastructure management, focused on EKS and cloud cost analysis.

## Features

- **EKS Management**: Query and manage EKS clusters across multiple AWS regions
- **Cost Analysis**: Get rough cost estimates for your infrastructure
- **Multi-Region Support**: Handle infrastructure across different AWS regions
- **Real-Time Queries**: Check cluster status, count, and configurations

## Quick Start

```bash
# Clone the repository
git clone <repository-url>
cd devops-agent

# Set up virtual environment
python -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

## Creates new backend configuration
xpander agent new --name "devops-agent" --framework "agno"

## Downloads the backend configurtion locally
xpander agent init "devops-agent"

## Runs the agent locally
xpander agent dev
```

## Example Usage

Ask the agent questions like:

- "How many EKS clusters do I have in us-west-2?"
- "How much does my production cluster cost?"
- "How do I configure EKS in multi-region?"
- "Calculate the rough cost of custom-workers-prod-cluster"

## Capabilities

✅ List EKS clusters by region  
✅ Provide AWS best practices guidance  
✅ Estimate infrastructure costs  
✅ Multi-region architecture advice  

## Requirements

- Python 3.8+
- AWS CLI configured with appropriate permissions
- Valid AWS credentials with EKS access

## License

MIT