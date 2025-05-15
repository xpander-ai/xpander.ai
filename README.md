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

xp = XpanderClient(api_key="YOUR_XPANDER_API_KEY")
agent = xp.agents.get("AGENT_ID")

response = agent.run("What's the latest revenue report?")
print(response)
```

### Step 3: Run an Agent with Any Framework

```python
# Example: Integrate LangChain, Semantic Kernel, or your own logic
from langchain.agents import initialize_agent

xp_tools = agent.get_tools()
lc_agent = initialize_agent(tools=xp_tools, llm=...)

# Or use stateful orchestration across frameworks
agent.orchestrate_with([lc_agent, other_agent])
```

---

## 🧩 Example Agents

| Framework      | Example                     | Link                                                                 |
|----------------|-----------------------------|----------------------------------------------------------------------|
| LangChain      | Customer support chatbot     | [Python Example](https://github.com/xpanderai/xpander/tree/main/examples/langchain_customer_support.py) |
| HuggingFace    | Image-to-text pipeline agent | [Python Example](https://github.com/xpanderai/xpander/tree/main/examples/huggingface_image_to_text.py) |
| Semantic Kernel| Calendar + Email orchestrator| [C# Example](https://github.com/xpanderai/xpander/tree/main/examples/semantic_kernel_calendar_email.cs) |

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