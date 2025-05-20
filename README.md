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

# Backend-as-a-Service for AI Agents**

<div align="center">
  <a href="https://github.com/xpander-ai/xpander.ai/blob/main/LICENSE"><img src="https://img.shields.io/github/license/xpander-ai/xpander.ai" alt="License"></a> <a href="https://pypi.org/project/xpander-sdk"><img src="https://img.shields.io/pypi/v/xpander-sdk" alt="PyPI Version"></a> <a href="https://npmjs.com/package/xpander-sdk"><img src="https://img.shields.io/npm/v/xpander-sdk" alt="NPM Version"></a> <a href="https://app.xpander.ai"><img src="https://img.shields.io/badge/Visit-xpander.ai-30a46c" alt="Platform Login"></a>
</div>

<div align="center">
  <p align="center">
<a href="https://x.com/xpander_ai"><img src="https://img.shields.io/badge/Follow%20on%20X-000000?style=for-the-badge&logo=x&logoColor=white" alt="Follow on X" /></a> <a href="https://www.linkedin.com/company/xpander-ai"><img src="https://img.shields.io/badge/Follow%20on%20LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white" alt="LinkedIn" /></a> <a href="https://discord.gg/CUcp4WWh5g"><img src="https://img.shields.io/badge/Join%20our%20Discord-5865F2?style=for-the-badge&logo=discord&logoColor=white" alt="Discord" /></a>
  </p>
</div>

---

xpander.ai helps developers give autonomous agents a backend—tools, memory, multi-user state, and Agent2Agent protocols—regardless of framework or vendor.


| Feature | Description |
|---------|-------------|
| 🛠️ **Framework Flexibility** | Choose from popular frameworks like OpenAI ADK, Agno, CrewAI, LangChain, or work directly with native LLM APIs |
| 🧰 **Tool Integration** | Access our comprehensive MCP-compatible tools library and pre-built integrations |
| 🚀 **Scalable Hosting** | Deploy and scale your agents effortlessly on our managed infrastructure |
| 💾 **State Management** | Opt for framework-specific local state or leverage our distributed state management system |
| ⚡ **Real-time Events** | Harness our event streaming capabilities for Slackbots, ChatUIs, Agent2Agent communication, and Webhook integrations |
| 🛡️ **API Guardrails** | Implement robust guardrails using our Agent-Graph-System to define and manage dependencies between API actions of tool-use |

By abstracting away infrastructure complexity, xpander.ai empowers you to focus on what matters most: building intelligent, effective, production-ready AI agents.

## 🌟 Featured Projects

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

## 📦 Installation

```bash
# Python
pip install xpander-sdk

# Node.js
npm install @xpander-ai/sdk

# CLI (for agent creation)
npm install -g xpander-cli
```

## 🚀 Quick Start

### Simple example with any LLM provider:

```python
from xpander_sdk import XpanderClient, Agent

# Init
xpander_client = XpanderClient(api_key="YOUR_XPANDER_API_KEY")  # Get your API key via `xpander login`
xpander_agent : Agent = xpander_client.agents.get(agent_id="YOUR_AGENT_ID")  # Get your agent ID via `xpander agent new`

# Initializing a new task creates a new conversation thread with empty state (messages object is empty)
xpander_agent.add_task("What can you do?")

# Run the agent loop
while not xpander_agent.is_finished:

    # Get LLM response with tools
    response = your_llm_provider.chat.completions.create(
        messages=xpander_agent.messages,  # Auto-translated to match the agent's state
        tools=xpander_agent.get_tools(),  # Auto-translated to match the agent's state
        tool_choice=xpander_agent.tool_choice 
    )
    
    # Execute tools automatically (agent stops when LLM calls the "finished" tool)
    xpander_agent.run_tools(xpander_agent.extract_tool_calls(response))

    # Optional: Manually stop agent execution
    # xpander_agent.stop_execution(is_success=True, result="Your result here")

# Get results
result = xpander_agent.retrieve_execution_result()
print(f"Answer: {result.result}")

# Continue the same conversation later with:
# agent.add_task("Follow-up question", thread_id=result.memory_thread_id)

# Or create a new conversation with add_task()
```

### Create Event-Driven Agents

```python
from xpander_utils.events import XpanderEventListener, AgentExecution, AgentExecutionResult

async def on_execution_request(execution_task: AgentExecution) -> AgentExecutionResult:
    # Your agent logic here
    your_agent = YourAnyFrameworkAgent()
    result = your_agent.invoke(execution_task.input)
    return AgentExecutionResult(result=result, is_success=True)

# Register event handler
listener = XpanderEventListener(**xpander_cfg)
listener.register(on_execution_request=on_execution_request)
```

### Framework Integration Examples

#### LlamaIndex

```python
from llama_index.agent import OpenAIAgent
from llama_index.llms import OpenAI

# Initialize with xpander tools and memory
agent = OpenAIAgent.from_tools(
    tools=xpander_agent.get_tools("llamaindex"),
    llm=OpenAI(model=xpander.get_model()),
    memory=xpander_agent.get_memory(agent.to_dict()),
    verbose=True
)

response = agent.chat("Your query here")
xpander_agent.send_result(response)
```

## 🧩 Hello World Example

The `Getting-Started/hello-world` directory contains a simple agent implementation to demonstrate core concepts:

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

### Running the Example

```bash
# Navigate to the hello-world example
cd Getting-Started/hello-world

## Python venv
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

## Agent creation
xpander login
xpander agent new

## Run the agent locally
python app.py                   # For CLI mode
# OR
python xpander_handler.py       # For event-driven mode
```

### Deploy to the Cloud

```bash
xpander deploy  # Will deploy the Docker container to the cloud and run it via the xpander_handler.py file
xpander logs    # Will stream logs locally from the agent configured locally
```

### Switching LLM Providers

```python
# In my_agent.py
llm_provider = LLMProvider.ANTHROPIC  # Or other supported providers

# During initialization
self.agent.select_llm_provider(llm_provider)  # This will convert the messages and tools objects to the specific LLM format

self.model_endpoint = AsyncAnthropicProvider()  # Add the actual implementation of the model invoke
```

## 🏗️ Core Features

## For developers; Accelerate agent development without infrastructure headaches

🚀 Deploy and run agents built with major frameworks and SDKs

🧠 Built-in agent memory & state persistence

🛠️ Use our tool library or generate tools from any API

⚙️ Visual agent workbench: tool dependencies, agent handovers, prompt tracing

📉 Tracing and logs: model thoughts, tool calls, payloads

🕹️ Trigger agents via MCP, A2A, Schedules, Slack, web UI and more

🔐 Bring your own LLM keys or use ours (securely stored)

💸 Faster + cheaper tool calling via optimized execution layer

☁️ Run agents in the cloud as easy as Docker Compose

## For agent platform owners; Manage and govern AI Agents centrally ➡️ platform engineering for AI Agents

📊 Single-pane-of-glass view of all agents in your org

🧱 Scaffolded agent templates for reusable workflows

🔐 Auth via OIDC, SAML, and context-aware user controls

🧭 Agent lifecycle: versioning, environment & deployment management

📦 Secure agent deployment in your VPC

📉 Export observability to your existing logging/monitoring stack

🌐 Self-hosted Agent Hub with A2A discovery

🔎 Tool calling policies & SLA enforcement per agent

🎯Centralized gateways for LLM integrations and API tool calling


## 📚 Documentation & Resources

- [Documentation](https://docs.xpander.ai)  
- [API Reference](https://docs.xpander.ai/api-reference/07-sdk)  
- [Example Library](https://github.com/xpander-ai/xpander.ai/tree/main/examples)  
- [Discord Community](https://discord.gg/CUcp4WWh5g)  

## ⚖️ License

- Open-source runtime: Apache License 2.0
- Hosted platform: Commercial (free tier available)

<p align="right">
    <a href="#readme-top">
        ↑ Back to Top ↑
    </a>
</p>
