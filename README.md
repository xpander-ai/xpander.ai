<h3 align="center">
  <a name="readme-top"></a>
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="images/Purple%20Logo%20White%20text.png">
    <img
      src="images/Purple%20Logo%20Black%20Text.png"
      style="max-width: 100%; height: auto; width: auto; max-height: 170px;"
      alt="xpander.ai Logo"
    >
  </picture>
</h3>

<div align="center">
  <h1>A framework-agnostic Backend for your AI Agents</h1>

  <a href="https://pepy.tech/projects/xpander-sdk"><img src="https://static.pepy.tech/badge/xpander-sdk/month"></a> 
  <a href="https://github.com/xpander-ai/xpander.ai/blob/main/LICENSE"><img src="https://img.shields.io/github/license/xpander-ai/xpander.ai" alt="License"></a> <a href="https://pypi.org/project/xpander-sdk"><img src="https://img.shields.io/pypi/v/xpander-sdk" alt="PyPI Version"></a> <a href="https://npmjs.com/package/xpander-sdk"><img src="https://img.shields.io/npm/v/xpander-sdk" alt="NPM Version"></a> <a href="https://app.xpander.ai"><img src="https://img.shields.io/badge/platform-login-30a46c" alt="Platform Login"></a>
</div>

<div align="center">
  <p align="center">
<a href="https://x.com/xpander_ai"><img src="https://img.shields.io/badge/Follow%20on%20X-000000?style=for-the-badge&logo=x&logoColor=white" alt="Follow on X" /></a> <a href="https://www.linkedin.com/company/xpander-ai"><img src="https://img.shields.io/badge/Follow%20on%20LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white" alt="LinkedIn" /></a> <a href="https://discord.gg/CUcp4WWh5g"><img src="https://img.shields.io/badge/Join%20our%20Discord-5865F2?style=for-the-badge&logo=discord&logoColor=white" alt="Discord" /></a>
  </p>
</div>

---

xpander.ai offers Backend-as-a-Service infrastructure for autonomous agents: memory, tools, multi-user state, various agent triggering options (MCP, A2A, API, Web interfaces), storage, agent-to-agent messaging — designed to support any agent framework and SDK


## Demo


https://github.com/user-attachments/assets/4db1fb71-b898-46f7-9b7c-2ec588b531fb



| Feature | Description |
|---------|-------------|
| 🛠️ **Framework Flexibility** | Choose from popular frameworks like OpenAI ADK, Agno, CrewAI, LangChain, or work directly with native LLM APIs |
| 🧰 **Tool Integration** | Access our comprehensive MCP-compatible tools library and pre-built integrations |
| 🚀 **Scalable Hosting** | Deploy and scale your agents effortlessly on our managed infrastructure |
| 💾 **State Management** | Opt for framework-specific local state or leverage our distributed state management system |
| ⚡ **Real-time Events** | Harness our event streaming capabilities for Slackbots, ChatUIs, Agent2Agent communication, and Webhook integrations |
| 🛡️ **API Guardrails** | Implement robust guardrails using our Agent-Graph-System to define and manage dependencies between API actions of tool-use |

By abstracting away infrastructure complexity, xpander.ai empowers you to focus on what matters most: building intelligent, effective, production-ready AI agents.

## ⭐ Featured template - fully-featured cloud-based SWE agent

1. Login to https://app.xpander.ai and go to the Templates section  
2. Deploy the Coding agent  
3. Send tasks to the agent.  
Examples:  
     ```
     Clone the <my-repo-name> repo and add the following feature to the codebase ..., then create a PR with the new code.
     ```
     ```
     Find all open PRs that have been waiting on review for more than 3 days.
     ```
4. Continue customizing, adding tools, configure triggering (MCP, A2A, Webhooks), multi-agent collaboration, and more.


<picture>
    <source media="(prefers-color-scheme: dark)" srcset="images/codingagent2.png">
    <img
      src="images/codingagent2.png"
      style="max-width: 100%; height: auto; width: auto; max-height: 170px;"
      alt="xpander.ai Logo"
    >
  </picture>

## Adding a backend to your agents in less than 5 minutes

## 📦 Installation

```bash
# Python
pip install xpander-sdk

# Node.js
npm install @xpander-ai/sdk

# CLI (for agent creation)
npm install -g xpander-cli
```

### Use xpander-cli to scaffold a new agent template

```bash
xpander login
xpander agent new
```

<img width="1062" alt="image" src="https://github.com/user-attachments/assets/a264fefe-ce22-420a-b105-9cd07b021c3e" />

### Prepare virtual env

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Develop the agent and run it
```
xpander dev
```

<img width="1175" alt="image" src="https://github.com/user-attachments/assets/29d2ea30-f9dd-498f-846a-6ce3cd897150" />

### Bring your AI agent code and stream events to your agent

Add one line of code to xpander_handler.py and your agent will be accessible via Agent2Agent, Slackbots, MCP servers, or WebUI.

```python xpander.handler.py
on_execution_request(execution_task: AgentExecution) -> AgentExecutionResult:
  your_agent.invoke(execution_task.input.text)
  return AgentExecutionResult(
        result="your-agent-result",
        is_success=True,
    ) 
```

### (Optional but highly recommended): Instrument your agent with AI tools and state management

```python
from xpander_sdk import XpanderClient, Agent

# Init the clients
xpander_client = XpanderClient(api_key="YOUR_XPANDER_API_KEY")
agent_backend : Agent = xpander_client.agents.get(agent_id="YOUR_AGENT_ID")  

# Initializing a new task creates a new conversation thread with empty agent state
xpander_agent.add_task("What can you do?")

response = openai_client.chat.completions.create(
      model="gpt-4o", 
      messages=agent_backend.messages,  # <-- Automatically loads the current state in the LLM format
      tools=agent_backend.get_tools(),  ## <-- Automatically loads all the tool schemas from the cloud
      tool_choice=agent_backend.tool_choice,
      temperature=0.0
  )
        
# Save the LLM Current state
agent.add_messages(response.model_dump())

# Extract the tools requested by the AI Model
tool_calls = XpanderClient.extract_tool_calls(llm_response=response.model_dump())

# Execute tools automatically and securely in the cloud after validating schema and loading user overrides and authentication
agent.run_tools(tool_calls=tool_calls)
```

### Deploy agent to the cloud

```bash
xpander deploy  # Will deploy the Docker container to the cloud and run it via the xpander_handler.py file
xpander logs    # Will stream logs locally from the agent configured locally
```

## 🌟 Featured Open Source AI Agents Using xpander.ai

<table>
  <tr>
    <th>Project</th>
    <th>Description</th>
    <th>License</th>
    <th>Tech Stack</th>
    <th>Link</th>
  </tr>
    <tr>
    <td>☸️ Agno EKS Agent</td>
    <td>Kubernetes operations agent with Agno framework, xpander backend, and AWS EKS MCP servers</td>
    <td>Apache 2.0</td>
    <td>Python, Agno, AWS EKS, MCP</td>
    <td><a href="https://github.com/xpander-ai/xpander.ai/tree/main/framework-examples/agno-agent">Repo</a></td>
  </tr>
  <tr>
    <td>💻 Coding Agent</td>
    <td>Framework-agnostic agent that reads, writes, and commits code to Git repositories</td>
    <td>MIT</td>
    <td>Python, OpenAI, Anthropic, Gemini, Llama 3</td>
    <td><a href="https://github.com/xpander-ai/coding-agent">Repo</a></td>
  </tr>
  <tr>
    <td>🎥 NVIDIA Meeting Recorder</td>
    <td>AI assistant that records, transcribes, and extracts insights from meetings</td>
    <td>Apache 2.0</td>
    <td>Python, NVIDIA SDKs, Speech Recognition</td>
    <td><a href="https://github.com/xpander-ai/nvidia-meeting-recorder-agent">Repo</a></td>
  </tr>
</table>

## 🧩 Getting Started Examples

The repository provides comprehensive examples to help you build AI agents with xpander.ai:

### Hello World Examples

Choose your preferred language to get started:

#### 🐍 Python Example
`Getting-Started/python/hello-world/` - A comprehensive Python implementation demonstrating:

```
python/hello-world/
├── app.py                      # CLI entry point for the agent
├── my_agent.py                 # Main agent implementation
├── my_agent.ipynb              # Jupyter notebook version
├── xpander_handler.py          # Event handler for platform events
├── agent_instructions.json     # Agent persona configuration
├── xpander_config.json         # API credentials configuration
├── Dockerfile                  # Container definition for deployment
├── providers/
│   ├── ai_frameworks/          # Framework integrations
│   └── llms/                   # LLM provider implementations
│       └── openai/             # OpenAI specific implementation
└── tools/
    ├── local_tools.py          # Custom tool implementations
    └── async_function_caller.py # Async function caller utility
```

#### 🟨 Node.js Example
`Getting-Started/node/hello-world/` - A Node.js implementation with camelCase conventions:

```
node/hello-world/
├── app.js                      # Main application entry point
├── MyAgent.js                  # Agent implementation class
├── package.json                # Node.js dependencies and scripts
├── xpander_config.json         # Xpander API configuration
├── agent_instructions.json     # Agent role and instructions
└── env.template               # Environment variables template
```

See individual README files in each directory for detailed setup instructions:
- [Python Hello World](Getting-Started/python/hello-world/README.md)
- [Node.js Hello World](Getting-Started/node/hello-world/README.md)

## 📚 Documentation & Resources

- [Documentation](https://docs.xpander.ai)  
- [API Reference](https://docs.xpander.ai/api-reference/07-sdk)  
- [Discord Community](https://discord.gg/CUcp4WWh5g)  

## ⚖️ License

- Open-source runtime: Apache License 2.0
- Hosted platform: Commercial (free tier available)

<p align="right">
    <a href="#readme-top">
        ↑ Back to Top ↑
    </a>
</p>
