<h3 align="center">
  <a name="readme-top"></a>
  <img
    src="https://raw.githubusercontent.com/xpanderai/xpander/main/img/xpander_logo.png"
    height="170"
    alt="xpander.ai Logo"
  >
</h3>

# **xpander.ai – Open-Source Multi-Framework Runtime for Autonomous AI Agents**

<div align="center">
  <a href="https://github.com/xpanderai/xpander/blob/main/LICENSE">
    <img src="https://img.shields.io/github/license/xpanderai/xpander" alt="License">
  </a>
  <a href="https://pypi.org/project/xpander-sdk">
    <img src="https://img.shields.io/pypi/v/xpander-sdk" alt="PyPI Version">
  </a>
  <a href="https://npmjs.com/package/@xpander-ai/sdk">
    <img src="https://img.shields.io/npm/v/@xpander-ai/sdk" alt="NPM Version">
  </a>
  <a href="https://xpander.ai">
    <img src="https://img.shields.io/badge/Visit-xpander.ai-30a46c" alt="Visit xpander.ai">
  </a>
</div>

<div align="center">
  <p align="center">
    <a href="https://x.com/xpanderai">
      <img src="https://img.shields.io/badge/Follow%20on%20X-000000?style=for-the-badge&logo=x&logoColor=white" alt="Follow on X" />
    </a>
    <a href="https://linkedin.com/company/xpanderai">
      <img src="https://img.shields.io/badge/Follow%20on%20LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white" alt="LinkedIn" />
    </a>
    <a href="https://discord.gg/xpanderai">
      <img src="https://img.shields.io/badge/Join%20our%20Discord-5865F2?style=for-the-badge&logo=discord&logoColor=white" alt="Discord" />
    </a>
  </p>
</div>

---

🚀 xpander.ai

Open-source, multi-framework runtime infrastructure for building, deploying, and scaling autonomous AI Agents.  
Bring your own AI frameworks, plug into any LLM, and deploy agents as real backend apps.

xpander.ai is the backbone for next-generation AI agent applications.  
The open-source runtime is your foundation; the hosted xpander.ai platform unlocks enterprise scale, security, and observability.

---

## 🌟 Why xpander?
- **Framework Agnostic:** LangChain, Semantic Kernel, Hugging Face, CrewAI, your custom agent — all work out of the box.
- **Production-Grade Runtime:** Agents run like backend services. Managed scheduling, memory, versioning, and multi-agent orchestration.
- **Build Faster, Safer:** Drop in tool libraries, generate new tools from any API, and control everything from a beautiful agent workbench or CI.
- **Observability Built-in:** Trace every thought, tool call, handoff, and model decision.

---

## ⚡ Quick Start


# Create new agents with xpander CLI

```
npm install -g xpander-cli
xpander login
xpander agent new
```

# Steam events from managed HMIs, add tools, and define complex multi-step multi-agent rules

```python xpander_handler.py
from xpander_utils.events import XpanderEventListener, AgentExecution, AgentExecutionResult ## pip install xpander_utils

async def on_execution_request(execution_task: AgentExecution) -> AgentExecutionResult:
    """
    Handles an execution request arriving via XpanderEventListener.
    Must be async‑def so the listener can await it without blocking.
    """

    your_agent = YourAnyFrameworkAgent()

    your_agent.invoke(execution_task.input)

    return AgentExecutionResult(result=error, is_success=False)

listener = XpanderEventListener(**xpander_cfg)
listener.register(on_execution_request=on_execution_request)
```

### Step 1: Install SDK

```bash
# Python
pip install xpander-sdk

# Node.js
npm install @xpander-ai/sdk
```

### Step 2: Connect to Your Agent

```python
from xpander_sdk import XpanderClient

agent = XpanderClient("XPANDER_API_KEY").agents.get("AGENT_ID")
print(agent.run("What's up, xpander? 🚀"))
```

### Integrate with Popular Frameworks

```python LlamaIndex
from llama_index.agent import OpenAIAgent
from llama_index.llms import OpenAI

query = "Hello, world! You are AI Agent with State managed by xpander.ai. You are now have access to more tools, authenticate users, and preserve state, return to tasks later"

# Initialize LlamaIndex agent with xpander tools and memory
agent = OpenAIAgent.from_tools(
    tools=xpander_agent.get_tools("llamaindex")
    llm=OpenAI(model=xpander.get_model()),
    memory=xpander_agent.get_memory(agent.to_dict()),
    verbose=True
)

# Run the query and send results
response = agent.chat(query)
xpander_agent.send_result(response)
```
---

## 🧩 Example Agents

| Framework      | Example                     | Link                                                                 |
|----------------|-----------------------------|----------------------------------------------------------------------|
| LangChain      | Customer support chatbot     | [Python Example](https://github.com/xpanderai/xpander/tree/main/examples/langchain_customer_support.py) |
| HuggingFace    | Image-to-text pipeline agent | [Python Example](https://github.com/xpanderai/xpander/tree/main/examples/huggingface_image_to_text.py) |
| Semantic Kernel| Calendar + Email orchestrator| [C# Example](https://github.com/xpanderai/xpander/tree/main/examples/semantic_kernel_calendar_email.cs) |

---

## 🚀 Hello World Agent

The xpander.ai repository includes a simple "Hello World" agent to help you get started with the framework. This example demonstrates core xpander.ai concepts and serves as a starting point for building your own agents.

### Features

- **Simple agent architecture**: Demonstrates an async agent loop pattern with the xpander SDK
- **Local tools integration**: Includes file reading and URL download capabilities
- **Multi-modal capabilities**: Can generate and display images in chat using markdown format
- **Two execution modes**:
  - Direct chat through command line interface (`app.py`)
  - Event-driven through xpander event listener (`xpander_handler.py`)

### Getting Started

1. Navigate to the `hello-world` directory
2. Install dependencies: `pip install -r requirements.txt`
3. Configure your agent by editing `xpander_config.json` with your API key and agent ID
4. Run the agent in interactive mode: `python app.py`
5. Alternatively, run the event listener mode: `python xpander_handler.py`

### Structure

- `app.py`: Entry point for interactive CLI mode
- `my_agent.py`: Core agent implementation using xpander SDK
- `xpander_handler.py`: Event-driven execution handler
- `tools/local_tools.py`: Definition of local tool functions
- `agent_instructions.json`: Configuration for agent personality and behavior

---

## 🏗️ Core Features

### For AI Agent Developers
- Managed AI Agent Runtime: Deploy and run agents as real backends (think Railway/Render, but for agents).
- Agentic Tooling: Massive tool library + instant tool generation from any OpenAPI spec.
- Multi-Agent Orchestration (A2A): Chain agents, handle handoffs, and orchestrate cross-runtime logic.
- Agent State & Memory: Built-in state machine, message history, and persistent memory.
- AI Agent Workbench: Visualize tool dependency graphs, debug payloads, run side-by-side model comparisons, and iterate fast.
- Optimized Tool Caller: Cut latency and LLM/API cost with a smarter, parallelized tool engine.
- Universal Triggers: Trigger agents via MCP, API, A2A, webhooks, or UI.
- Integrations to Human Interfaces: Slack, Teams, ChatGPT-like UI, scheduled workflows, and more.
- Observability/Trace: Step-by-step, end-to-end analysis of execution, model decisions, API requests, and tool results.
- Bring Your Own Keys: Use your own LLM API keys (OpenAI, Anthropic, Mistral, etc.), or secure vault keys via xpander.
- Agent Lifecycle Management: Versioning, staging, production rollouts, and A/B testing built in.

### For Platform Owners
- Single Pane of Glass: Manage all agents org-wide with one dashboard.
- Enterprise Auth: OIDC/SAML support, RBAC, and audit trails.
- Scaffolded Templates: Quickly configure agents using framework-agnostic templates.
- A/B Testing: Compare frameworks, LLM vendors, or agent strategies in production.
- Agent Hub: Self-hosted or managed, with full discovery and internal sharing.
- LLM Gateway: Centralize LLM access, model switching, and fine-grained API controls.
- Compute Environment Management: Launch agents in your own VPC or on xpander-managed cloud.
- Observability Data Export: Ship logs to your SIEM or central logging.
- SLA Management: Treat agents like production services with clear SLOs and guarantees.
- Controlled Tool Gateway: API/network-level guardrails and approval workflows.

---

## 🌐 Ecosystem

| Feature                | Open-Source Runtime | Hosted Platform         |
|------------------------|---------------------|------------------------|
| Agent Execution        | ✅                  | ✅                     |
| Tool Library           | ✅                  | ✅                     |
| Observability          | ⚠️ (logs only)      | ✅ (trace, UI)          |
| Management UI          | ❌                  | ✅                     |
| Templates & Workbench  | ❌                  | ✅                     |
| Auth/SLA/RBAC          | ❌                  | ✅                     |
| Enterprise Support     | ❌                  | ✅                     |

---

## 📚 Documentation

- [Docs](https://docs.xpander.ai)  
- [API Reference](https://docs.xpander.ai/api)  
- [Agent Framework Examples](https://github.com/xpanderai/xpander/tree/main/examples)  
- [Community](https://discord.gg/xpanderai)  

---

## 🤝 Contribute

We welcome contributions!  
Read our contributing guide and join the community.

---

## ⚖️ License

AGPL-3.0 for the open-source runtime.  
Hosted platform is commercial with free tier available.

---

<p align="right" style="font-size: 14px; color: #555; margin-top: 20px;">
    <a href="#readme-top" style="text-decoration: none; color: #007bff; font-weight: bold;">
        ↑ Back to Top ↑
    </a>
</p>

---

xpander.ai — The backend for serious AI Agent developers.

> No vendor lock-in. No black boxes. Build, scale, and own your agent-powered future.