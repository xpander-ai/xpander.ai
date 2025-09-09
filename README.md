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
  <h3>
    <font size="7">Full-stack platform for AI Agents</font>
  </h3>
</div>


<div align="center">
<hr/>
  <a href="https://www.producthunt.com/products/xpander-ai?embed=true&utm_source=badge-top-post-badge&utm_medium=badge&utm_source=badge-xpander&#0045;ai&#0045;2" target="_blank">
    <img src="https://api.producthunt.com/widgets/embed-image/v1/top-post-badge.svg?post_id=1009903&theme=light&period=daily&t=1756801389318" alt="xpander&#0046;ai - Backend&#0032;and&#0032;Frontend&#0032;for&#0032;your&#0032;AI&#0032;Agents | Product Hunt" style="width: 250px; height: 54px;" width="250" height="54" />
  </a>
</div>


<div align="center">
  <a href="https://pepy.tech/projects/xpander-sdk"><img src="https://static.pepy.tech/badge/xpander-sdk/month"></a> 
  <a href="https://github.com/xpander-ai/xpander.ai/blob/main/LICENSE"><img src="https://img.shields.io/github/license/xpander-ai/xpander.ai" alt="License"></a> <a href="https://pypi.org/project/xpander-sdk"><img src="https://img.shields.io/pypi/v/xpander-sdk" alt="PyPI Version"></a> <a href="https://npmjs.com/package/xpander-sdk"><img src="https://img.shields.io/npm/v/xpander-sdk" alt="NPM Version"></a> <a href="https://app.xpander.ai"><img src="https://img.shields.io/badge/platform-login-30a46c" alt="Platform Login"></a>
</div>

<div align="center">
  <p align="center">
<a href="https://x.com/xpander_ai"><img src="https://img.shields.io/badge/Follow%20on%20X-000000?style=for-the-badge&logo=x&logoColor=white" alt="Follow on X" /></a> <a href="https://www.linkedin.com/company/xpander-ai"><img src="https://img.shields.io/badge/Follow%20on%20LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white" alt="LinkedIn" /></a> <a href="https://discord.gg/CUcp4WWh5g"><img src="https://img.shields.io/badge/Join%20our%20Discord-5865F2?style=for-the-badge&logo=discord&logoColor=white" alt="Discord" /></a>
  </p>
</div>

---

xpander.ai is Backend-as-a-Service for autonomous agents. It abstracts the ops layer so AI engineers focus on behavior and outcomes. You get managed agent hosting with version control and CI/CD, a fully managed PostgreSQL memory layer, and a curated library of 2,000+ functions, including MCP Tools and the MCP Generator.

Our AI native triggering system post-processes inputs from MCP, agent-to-agent, API, and web, then delivers a single unified message to your agent so you never deal with wiring or formats. xpander works with any agent framework or SDK, with native support for Agno and OpenAI.

| Feature                     | Description                                                                                                                |
| --------------------------- | -------------------------------------------------------------------------------------------------------------------------- |
| 🛠️ **Framework Flexibility** | Choose from popular frameworks like OpenAI ADK, Agno, CrewAI, LangChain, or work directly with native LLM APIs             |
| 🧰 **Tool Integration**      | Access our comprehensive MCP-compatible tools library and pre-built integrations                                           |
| 🚀 **Scalable Hosting**      | Deploy and scale your agents effortlessly on our managed infrastructure                                                    |
| 💾 **State Management**      | Opt for framework-specific local state or leverage our distributed state management system                                 |
| ⚡ **Real-time Events**      | Harness our event streaming capabilities for Slackbots, ChatUIs, Agent2Agent communication, and Webhook integrations       |
| 🛡️ **API Guardrails**        | Implement robust guardrails using our Agent-Graph-System to define and manage dependencies between API actions of tool-use |

By abstracting away infrastructure complexity, xpander.ai empowers you to focus on what matters most: building intelligent, effective, production-ready AI agents.

## ⭐ Featured template - fully-featured cloud-based SWE agent with Claude Code

1. [Template url](https://app.xpander.ai/templates/f3240158-28ca-4c8b-96c8-a215246002dc)
2. Send tasks to the agent.  
Examples:  
     ```
     Clone the <my-repo-name> repo and add the following feature to the codebase ..., then create a PR with the new code.
     ```
     ```
     Find all open PRs that have been waiting on review for more than 3 days.
     ```
3. Continue customizing, adding tools, configure triggering (MCP, A2A, Webhooks), multi-agent collaboration, and more.


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
from xpander_sdk import Task, Backend, on_task
from agno.agent import Agent

# Stateful agent, zero infrastructure overhead
@on_task
async def handle_task(task: Task):
  backend = Backend() # DB, MCP tools, system prompt
  agent = Agent(**await backend.aget_args())

  # Task includes user data + events from Slack, webhooks, agents
  result = await agent.arun(message=task.to_message())
  task.result = result.content
  return task
```

### Deploy agent to the cloud

```bash
xpander deploy  # Will deploy the Docker container to the cloud and run it via the xpander_handler.py file
xpander logs    # Will stream logs locally from the agent configured locally
```

## 🧩 Getting Started Examples

[simple-hello-world](https://docs.xpander.ai/Examples/01-simple-hello-world)

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
