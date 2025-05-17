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

# **xpander.ai – Backend-as-a-Service for AI Agents**

<div align="center">
  <a href="https://github.com/xpander-ai/xpander.ai/blob/main/LICENSE">
    <img src="https://img.shields.io/github/license/xpander-ai/xpander.ai" alt="License">
  </a>
  <a href="https://pypi.org/project/xpander-sdk">
    <img src="https://img.shields.io/pypi/v/xpander-sdk" alt="PyPI Version">
  </a>
  <a href="https://npmjs.com/package/xpander-sdk">
    <img src="https://img.shields.io/npm/v/xpander-sdk" alt="NPM Version">
  </a>
  <a href="https://app.xpander.ai">
    <img src="https://img.shields.io/badge/Visit-xpander.ai-30a46c" alt="Platform Login">
  </a>
</div>

<div align="center">
  <p align="center">
    <a href="https://x.com/xpander_ai">
      <img src="https://img.shields.io/badge/Follow%20on%20X-000000?style=for-the-badge&logo=x&logoColor=white" alt="Follow on X" />
    </a>
    <a href="https://www.linkedin.com/company/xpander-ai">
      <img src="https://img.shields.io/badge/Follow%20on%20LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white" alt="LinkedIn" />
    </a>
    <a href="https://discord.gg/CUcp4WWh5g">
      <img src="https://img.shields.io/badge/Join%20our%20Discord-5865F2?style=for-the-badge&logo=discord&logoColor=white" alt="Discord" />
    </a>
  </p>
</div>

---

xpander.ai is a backend-as-a-service platform designed specifically for AI agents. Our production-grade infrastructure seamlessly integrates with leading AI frameworks including CrewAI, Huggingface and LlamaIndex, as well as direct LLM vendor APIs from OpenAI, Amazon Bedrock, and Nvidia. The platform offers a modular approach to building your agentic stack:

- **Framework Flexibility**: Choose from popular frameworks like OpenAI ADK, Agno, CrewAI, LangChain, or work directly with native LLM APIs
- **Tool Integration**: Access our comprehensive MCP-compatible tools library and pre-built integrations
- **Scalable Hosting**: Deploy and scale your agents effortlessly on our managed infrastructure
- **State Management**: Opt for framework-specific local state or leverage our distributed state management system
- **Real-time Events**: Harness our event streaming capabilities for Slackbots, ChatUIs, Agent2Agent communication, and Webhook integrations
- **API Guardrials**: Implement robust guardrails using our Agent-Graph-System to define and manage dependencies between API actions of tool-use

By abstracting away infrastructure complexity, xpander.ai empowers you to focus on what matters most: building intelligent, effective AI agents.

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

### Connect to an Agent

```python
from xpander_sdk import XpanderClient

# Initialize and call your agent
agent = XpanderClient("XPANDER_API_KEY").agents.get("AGENT_ID")
result = agent.run("What can you do for me?")
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

The `hello-world` directory contains a minimalist agent implementation to demonstrate core concepts:

```
hello-world/
├── app.py                    # CLI entry point
├── my_agent.py               # Agent implementation
├── xpander_handler.py        # Event handler
├── tools/
│   └── local_tools.py        # Custom tools
└── agent_instructions.json   # Agent configuration
```

### Running the Example

```bash
cd hello-world
pip install -r requirements.txt
python app.py                 # For CLI mode
# OR
python xpander_handler.py     # For event-driven mode
```

### Switching LLM Providers

```python
# In my_agent.py
llm_provider = LLMProvider.ANTHROPIC  # Or other supported providers

# During initialization
self.agent.select_llm_provider(llm_provider)  # This will convert the messages and tools object to the specific LLM format

self.model_endpoint = AsyncAnthropicProvider()  # Add the actual implementation of the model invoke
```

## 🏗️ Core Features

### Development Features
- **Framework Agnostic**: Support for LangChain, Semantic Kernel, HuggingFace, CrewAI, and custom agents
- **Tool Management**: Drop-in tool libraries and auto-generation from OpenAPI specs
- **LLM Flexibility**: Connect to any LLM (OpenAI, Anthropic, Mistral, etc.)
- **State & Memory**: Built-in state machine, message history, and persistent memory
- **Multi-Agent Orchestration**: Chain agents, handle handoffs, and manage cross-runtime logic

### Infrastructure Features
- **Runtime Environment**: Deploy agents as real backend services
- **Observability**: Trace every step of execution, model decisions, and tool calls
- **Multiple Triggers**: API, webhooks, UI, or inter-agent communication
- **UI Integrations**: Slack, Teams, web interfaces, and more
- **Versioning & Lifecycle**: Staging, production rollouts, and A/B testing


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