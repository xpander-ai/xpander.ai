# Agno + xpander.ai + AWS MCP Example

Simple example integrating **Agno agents** with **Xpander backend** and **AWS EKS MCP servers**.

## Quick Start

```bash
# Install Xpander CLI
pip install xpander-cli

# Login and create project
xpander login
xpander agent new ## or init -- follow the wizard and call it eks-agent

pip install -r requirements.txt

# Add OpenAI key to .env
echo "OPENAI_API_KEY=your_key" > .env

# Copy this example's files to your project
# Run
python xpander_handler.py
```

## What it does

- **Agno agent** with conversation history and state management
- **Xpander WebSocket** event handling  
- **AWS EKS MCP servers** for Kubernetes operations

## Key Files

- `myCoolAgnoAgent.py` - Agno agent implementation
- `xpander_handler.py` - WebSocket event handler
- `agent_instructions.json` - Agent behavior config

## Usage

When you run the handler, you'll see output like this:

```bash
❯ python xpander_handler.py
2025-06-16 02:33:54.934 | DEBUG    | xpander_utils.events.listener:__init__:102 - XpanderEventListener initialised (base_url=https://inbound.xpander.ai, org_id=bbe95a5a-a157-4657-a879-c8e6b02f0f87, retries=5)
2025-06-16 02:33:55.908 | INFO     | xpander_utils.events.listener:start:130 - Listener started; waiting for events…
2025-06-16 02:33:57.249 | INFO     | xpander_utils.events.listener:_register_agent_worker:346 - Agent 'EKS Post-Mortem Analyst' chat: https://green-mink.agents.xpander.ai | builder: https://app.xpander.ai/agents/a22a3372-9555-445c-a239-1c7ef8663fff
```

The output shows two important URLs:
- **Chat UI**: Use this to send events and interact with your agent
- **Builder UI**: Use this to configure your agent settings

Ask questions through the chat UI:
- "List pods in default namespace"
- "Show nginx service status" 
- "Get cluster nodes"

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
