# Complete Tutorial: Building a Fully Local AI Agent

This tutorial shows how to create a completely local, open-source AI agent using **xpander.ai**, **Agno**, and **Ollama** with open-source models. No external LLM APIs required.

## Architecture Overview

The stack consists of:

- **xpander.ai**: Backend platform providing runtime, storage, tools, and lifecycle management
- **Agno**: Multi-agent framework with tool support
- **Ollama**: Local LLM runtime for open-source models
- **Docker**: Containerized deployment

**xpander.ai Backend Benefits:**

- **Runtime**: Handles agent execution and task orchestration
- **Storage**: Persistent data and conversation history
- **Tools**: Add/manage tools via app.xpander.ai dashboard
- **Lifecycle**: Deploy to cloud with `xpander agent deploy`
- **Management**: Full agent monitoring and configuration through web interface
- **Event System**: SSE-based task delivery to `@on_task` decorator
- **Multi-Source**: Receive tasks from WebUI, Slack, API without infrastructure handling
- **Prompt Management**: System prompts managed centrally via dashboard

## Prerequisites

1. **Install xpander.ai CLI**

```bash
npm install -g xpander-cli
```

1. **Install Ollama**

```bash
# macOS
brew install ollama
# Linux
curl -fsSL https://ollama.ai/install.sh | sh
```

1. **Pull an Open Source Model**

```bash
ollama pull gpt-oss:20b
# Or use other models like:
# ollama pull llama3.2:3b
# ollama pull mistral:7b
```

1. **Start Ollama Service**

```bash
ollama serve
```

## Project Setup

### Step 1: Create New Agent Project

```bash
x a n --name "local-agent" --framework agno --folder .
```

The `x a n` command (shortcut for `xpander agent new`) automatically generates the complete project structure:

- `xpander_handler.py` - Main agent logic
- `requirements.txt` - Python dependencies  
- `.env` - Pre-configured environment with your Xpander credentials
- `.env.example` - Environment template
- `Dockerfile` - Container configuration

### Step 2: Environment Already Configured

The `.env` file is automatically created and populated with your Xpander credentials during the `x a n` command. No manual configuration needed - it contains:

```bash
XPANDER_API_KEY="{YOUR_API_KEY}"
XPANDER_ORGANIZATION_ID="{YOUR_ORGANIZATION_ID}"
XPANDER_AGENT_ID="{YOUR_XPANDER_AGENT_ID}"
```

### Step 3: Install Dependencies

Create virtual environment and install packages:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Key Files Explained

### xpander_handler.py

The core agent implementation that connects all components and handles events:

```python
from dotenv import load_dotenv
load_dotenv()

from xpander_sdk import Task, Backend, on_task, OutputFormat, Tokens
from pydantic import BaseModel
from agno.agent import Agent
from agno.models.ollama import Ollama

@on_task  # SSE event listener for tasks from any source
async def my_agent_handler(task: Task):
    backend = Backend(configuration=task.configuration)
   
    # Configure agent with local Ollama model
    agno_agent = Agent(**backend.get_args(override={
        'model': Ollama(id="gpt-oss:20b")  # Local model
    }))
    
    result = await agno_agent.arun(message=task.to_message())
    
    # Handle structured output
    if task.output_format == OutputFormat.Json and isinstance(result.content, BaseModel):
        result.content = result.content.model_dump_json()
    
    task.result = result.content
    
    # Report metrics
    task.tokens = Tokens(
        prompt_tokens=sum(result.metrics['input_tokens']),
        completion_tokens=sum(result.metrics['completion_tokens'])
    )
    task.used_tools = [tool.tool_name for tool in result.tools]
    
    return task
```

**Key Architecture Points:**

- `@on_task` decorator receives events via Server-Sent Events (SSE)
- Tasks can originate from WebUI, Slack, API calls, or any configured source
- Agent handles all task routing and infrastructure automatically
- System prompts and configuration managed via app.xpander.ai dashboard

### requirements.txt

Essential dependencies for the local agent:

```txt
python-dotenv
agno[all]
xpander-sdk[agno]
ollama
openai
```

### Dockerfile

Multi-stage build for production deployment:

```dockerfile
FROM python:3.12-alpine AS builder

WORKDIR /usr/src/app

# Install system dependencies
RUN apk add --no-cache \
    curl bash gcc g++ libffi-dev musl-dev \
    openssl-dev make python3-dev rust cargo \
    git nodejs npm ca-certificates

COPY . .

# Create virtual environment
RUN python3 -m venv .venv
ENV PATH="/usr/src/app/.venv/bin:$PATH"

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

CMD ["python", "xpander_handler.py"]
```

## Running the Agent

### Local Development

```bash
source .venv/bin/activate
python xpander_handler.py
```

### Docker Deployment

```bash
# Build image
docker build . -t local-agent

# Run container with Ollama connection
docker run --name local-agent -d \
  -e OLLAMA_HOST=http://host.docker.internal:11434 \
  --env-file .env \
  local-agent
```

Expected output:

```bash
❯ docker logs local-agent
2025-09-07 18:24:29.746 | DEBUG    | xpander_sdk.modules.events.events_module:__init__:132 - Events initialised (base_url=https://inbound.xpander.ai, org_id=8d185373-8b24-47a7-8607-3e9036b968bb, retries=5)
2025-09-07 18:24:30.188 | INFO     | xpander_sdk.modules.events.events_module:start:172 - Listener started; waiting for events…
2025-09-07 18:24:31.043 | INFO     | xpander_sdk.modules.events.events_module:register_agent_worker:406 - Worker registered – id=b229a189-b7ad-413b-8d26-baae751737d1
2025-09-07 18:24:31.044 | INFO     | xpander_sdk.modules.events.events_module:register_agent_worker:427 - Agent 'local-agent' chat: https://salmon-harrier.agents.xpander.ai | builder: https://app.xpander.ai/agents/2daa6180-8f91-4003-a6b2-c3569833acd3
```

## Testing the Agent

Invoke your local agent:

```bash
x a invoke "local-agent" "hi, are you there?"
```

Expected output:

```bash
✔ Using agent: local-agent (2daa6180-8f91-4003-a6b2-c3569833acd3)
✔ Response received

🤖 Agent Response:
──────────────────────────────────────────────────
Hello! Yes, I'm here. How can I help you today?
──────────────────────────────────────────────────

Response time: 2855ms
```

### Verify Local Model Usage

During execution, verify the model is loaded locally:

```bash
❯ ollama ps
NAME           ID              SIZE     PROCESSOR    CONTEXT    UNTIL              
gpt-oss:20b    aa4295ac10c3    17 GB    100% GPU     131072     4 minutes from now    
```

Check agent task processing in Docker logs:

```bash
❯ docker logs local-agent
2025-09-07 18:24:29.746 | DEBUG    | Events initialised (base_url=https://inbound.xpander.ai)
2025-09-07 18:24:30.188 | INFO     | Listener started; waiting for events…
2025-09-07 18:24:31.043 | INFO     | Worker registered
2025-09-07 18:24:31.044 | INFO     | Agent 'local-agent' ready
2025-09-07 18:25:41.049 | INFO     | Handling task 0d380195-f81a-4be3-b5f1-4b9c635dfecf
2025-09-07 18:25:49.074 | INFO     | Finished handling task 0d380195-f81a-4be3-b5f1-4b9c635dfecf
```

## Architecture Benefits

### Complete Privacy

- All processing happens locally
- No data sent to external LLM providers
- Full control over model and data

### Open Source Stack

- **Ollama**: MIT licensed local LLM runtime
- **Agno**: Open source multi-agent framework
- **Various models**: Llama, Mistral, CodeLlama, etc.

### Production Ready

- Docker containerization
- Scalable architecture via Xpander backend
- Metrics and observability built-in
- Tool integration support

## Xpander Backend Management

Once your agent is running, you can leverage Xpander's backend platform:

### Agent Control Plane (app.xpander.ai)

- **Tool Management**: Add/remove tools for your agent
- **Storage Access**: View conversation history and persistent data
- **Configuration**: Modify agent settings and parameters
- **Monitoring**: Track usage metrics and performance
- **System Prompts**: Centrally manage and update agent prompts
- **Task Sources**: Configure WebUI, Slack, API endpoints, and webhooks
- **Event Routing**: All sources automatically route to your `@on_task` handler

### Cloud Deployment

Deploy your local agent to xpander.ai's cloud infrastructure:

```bash
xpander agent deploy
```

This moves your agent from local development to cloud production while maintaining the same codebase and configuration.

### Hybrid Architecture

- **Local Development**: Run agent locally with Ollama for privacy and testing
- **Cloud Production**: Deploy to xpander.ai cloud with same local models  
- **Unified Management**: Single dashboard for all environments
- **Seamless Migration**: Same code works locally and in cloud

## Advanced Configuration

### Custom Models

Modify `xpander_handler.py` to use different models:

```python
# Lightweight option
'model': Ollama(id="llama3.2:3b")

# Balanced performance  
'model': Ollama(id="mistral:7b")

# Code-focused
'model': Ollama(id="codellama:13b")
```

### Tool Integration

Add tools to your agent via the xpander.ai dashboard - they automatically become available to your `@on_task` handler without code changes.
