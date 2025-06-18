# Agno + xpander.ai + AWS MCP Example

Simple example integrating **Agno agents** with **Xpander backend** and **AWS EKS MCP servers**.

## Quick Start

```bash
# Install Xpander CLI
npm install -g xpander-cli

# Login and create project
xpander login
xpander agent new ## or init -- follow the wizard and call it eks-agent 

## Important: The init can override local files, make sure to copy & paste the xpander_handler from this repo
```

## Running (CLI Mode)

You can run either agent locally in CLI mode using Python. This is useful for quick testing and development.

### 1. (Recommended) Create and activate a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 2. Run the agent:

- **Standalone agent:**
  ```bash
  python agno_agent.py
  ```
- **Xpander backend agent:**
  ```bash
  python agno_agent_with_backend.py
  ```

https://github.com/user-attachments/assets/4975ec55-617f-4c3f-9f3b-3b9cd073186f



Both scripts will run in CLI mode and output results to your terminal.

### 3. Stream events (A2A, MCP, Slack, WebUI) to your agent

To enable event streaming and integration with Xpander's backend and external services, run:

```bash
python xpander_handler.py
```

**Important:** Ensure you have EKS access configured correctly. Adjust the AWS profile or IAM keys in the MCP configuration as needed.

## What it does

- **Agno agent** with conversation history and state management
- **Xpander WebSocket** event handling  
- **AWS EKS MCP servers** for Kubernetes operations

## Xpander Backend: Value & Comparison

This example includes two agent implementations:

- [`agno_agent.py`](./agno_agent.py): **Standalone Agno agent**
- [`agno_agent_with_backend.py`](./agno_agent_with_backend.py): **Agno agent integrated with Xpander backend**

### Standalone Agent (`agno_agent.py`)
- Runs locally with basic state and history management.
- Uses Agno's built-in tools and OpenAI models.
- **Limitations:**
  - No persistent storage or advanced session management.
  - No integration with Xpander's cloud features (e.g., chat UI, analytics, multi-user support).
  - Lacks organization-wide agent management and deployment.

### Xpander Backend Agent (`agno_agent_with_backend.py`)
- Integrates with the Xpander backend via the `AgnoAdapter`.
- Inherits all standalone features **plus**:
  - **Persistent storage** of chat history, state, and sessions.
  - **Multi-user and multi-session support** out of the box.
  - **Web-based Chat UI** and agent builder for easy interaction and configuration.
  - **Centralized analytics, monitoring, and logging** for all agent activity.
  - **Easy deployment** to Xpander's cloud infrastructure (scaling, monitoring, production readiness).
  - **Customizable system prompts, tools, and storage** via the backend.

## Key Files

- `myCoolAgnoAgent.py` - Agno agent implementation
- `xpander_handler.py` - WebSocket event handler
- `agent_instructions.json` - Agent behavior config

## Usage

When you run `xpander_handler.py`, you'll see output like this:

```bash
❯ python xpander_handler.py
2025-06-16 02:33:54.934 | DEBUG    | xpander_utils.events.listener:__init__:102 - XpanderEventListener initialised (base_url=https://inbound.xpander.ai, org_id=bbe95a5a-a157-4657-a879-c8e6b02f0f87, retries=5)
2025-06-16 02:33:55.908 | INFO     | xpander_utils.events.listener:start:130 - Listener started; waiting for events…
2025-06-16 02:33:57.249 | INFO     | xpander_utils.events.listener:_register_agent_worker:346 - Agent 'EKS Post-Mortem Analyst' chat: https://green-mink.agents.xpander.ai | builder: https://app.xpander.ai/agents/a22a3372-9555-445c-a239-1c7ef8663fff
```

The output shows two important URLs:
- **Chat UI**: Use this to send events and interact with your agent
- **Builder UI**: Use this to configure your agent settings


https://github.com/user-attachments/assets/bdf676df-a970-4b28-8a65-9a28cbca630b


Ask questions through the chat UI:
- "List pods in default namespace"
- "Show nginx service status" 
- "Get cluster nodes"

One cool example

<img width="961" alt="slack" src="https://github.com/user-attachments/assets/af5347d9-3cf4-41d8-a5f6-487aa53bf020" />
<img width="915" alt="image" src="https://github.com/user-attachments/assets/06b89516-9658-4c02-a1a0-815f824e3d7d" />


## Deployment

Once you've tested your agent locally and it's working as expected:

```bash
xpander deploy
```

Follow the deployment wizard to:
- Configure your production environment
- Set up scaling and monitoring
- Deploy your agent to Xpander's cloud infrastructure

That's it! 
