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
python xpander_handler.py  # <-- Events with entry point for your agents
```

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
  <tr>
    <td>🌍 Hello World Example</td>
    <td>Simple starter template for building agents with xpander.ai</td>
    <td>Apache 2.0</td>
    <td>Python, OpenAI</td>
    <td><a href="https://github.com/xpander-ai/xpander.ai/tree/main/examples/hello-world">Repo</a></td>
  </tr>
</table>

## 🧩 Hello World Example

The `Getting-Started/hello-world` directory contains a simple agent implementation to demonstrate core concepts of how to run asynchronous AI Agents with local tools and cloud tools, and a fully managed stateful state in a backend with xpander.ai:

```
hello-world/
├── app.py                      # CLI entry point for the agent with local thread
├── my_agent.py                 # Agent implementation (Your agent code goes here)
├── xpander_handler.py          # Event handler for incoming events from the platform
├── Dockerfile                  # For containerized deployment
├── providers/
│   ├── ai_frameworks/          # Framework integrations
│   └── llms/                   # LLM provider implementations
│       ├── openai/             # OpenAI specific implementation
│       └── ...
└── tools/
    ├── local_tools.py          # Custom tools implementation
    └── async_function_caller.py # Async function caller utility
```

See [Hello-world.md](Getting-Started/hello-world/README.md) for more details

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
