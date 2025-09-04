# LangChain + xpander.ai Integration

A comprehensive example demonstrating how to integrate **LangChain** with **xpander.ai** to create powerful AI agents with access to pre-built tools and services.

🚀 **Quick Start**: [Import this template](https://app.xpander.ai/templates/13de363d-c947-41d9-a25a-3e94d2fad90f) directly into xpander.ai

## Features

- **🦜 LangChain Integration**: Seamless integration with LangChain ecosystem
- **🧰 Pre-built Tools**: Access to Tavily Search and Email sending capabilities
- **⚡ ReAct Agent**: Uses LangGraph's ReAct agent pattern for intelligent tool usage
- **📋 System Instructions**: Automatically extracts and applies xpander.ai agent instructions as system prompts
- **🔍 Advanced Filtering**: Configurable output schema filtering for optimized responses
- **🛡️ Environment Validation**: Built-in validation for required credentials
- **📊 Token Optimization**: Smart filtering to reduce token usage and costs

## Quick Start

### Prerequisites

- **xpander.ai account required**: [Sign up here](https://app.xpander.ai)
- Python 3.8+
- OpenAI API key
- xpander.ai API credentials

### Installation

```bash
# Clone the repository (or navigate to the example)
cd framework-examples/langchain

# Install dependencies
pip install "xpander-sdk" "langchain[openai]" langgraph python-dotenv
```

### Environment Setup

Create a `.env` file with your credentials:

```env
# Required - OpenAI API
OPENAI_API_KEY="your_openai_api_key"

# Required - xpander.ai Platform Configuration
XPANDER_API_KEY="your_xpander_api_key"
XPANDER_ORGANIZATION_ID="your_organization_id"
XPANDER_AGENT_ID="your_agent_id"
```

**Where to find your xpander.ai credentials:**

1. **API Key**: Go to [xpander.ai Settings](https://app.xpander.ai) → Settings → API Keys
2. **Organization ID**: Found in your organization id and API Key
3. **Agent ID**: Create or select an agent in the xpander.ai platform

### Run the Example

```bash
# Option 1: Run the Jupyter notebook
jupyter notebook xpander_langchain_example.ipynb

# Option 2: Run as Python script
python -c "
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent
from xpander_sdk import Agents

load_dotenv()

# Initialize xpander agent
agent_config = Agents().get(agent_id=os.getenv('XPANDER_AGENT_ID'))

# Create LangChain ReAct agent
llm = ChatOpenAI(model=agent_config.model_name, temperature=0)
agent = create_react_agent(llm, agent_config.tools.functions)

# Test the agent
response = agent.invoke({'messages': [('user', 'search for information about xpander.ai')]})
print(response)
"
```

## Example Usage

The example demonstrates various use cases:

### Using xpander Agent Instructions

```python
# Extract system prompt from xpander agent instructions
def create_system_prompt(instructions):
    """Convert xpander agent instructions to system prompt"""
    parts = []
    
    if hasattr(instructions, 'general') and instructions.general:
        parts.append(f"System: {instructions.general}")
    
    if hasattr(instructions, 'goal_str') and instructions.goal_str:
        parts.append(f"Goals:\n{instructions.goal_str}")
    
    if hasattr(instructions, 'instructions') and instructions.instructions:
        instr_list = "\n".join([f"- {instr}" for instr in instructions.instructions])
        parts.append(f"Instructions:\n{instr_list}")
    
    return "\n\n".join(parts)

# Create a ReAct agent with xpander tools and system prompt
agent = create_react_agent(
    llm, 
    xpander_agent.tools.functions,
    state_modifier=SystemMessage(content=create_system_prompt(xpander_agent.instructions))
)
```

### Web Search with Filtering
```python
# Agent automatically uses Tavily Search with output filtering
response = agent.invoke({
    "messages": [("user", "search for the latest AI trends")]
})
```

### Email Sending
```python
# Agent can send emails when configured
response = agent.invoke({
    "messages": [("user", "send an email summary of the search results to team@company.com")]
})
```

### Multi-step Workflows
```python
# Agent can chain tools together
response = agent.invoke({
    "messages": [("user", "search for company news, summarize the findings, and email the summary")]
})
```

## Available Tools

This example includes two pre-configured tools:

| Tool | Description | Features |
|------|-------------|----------|
| 🔍 **Tavily Search** | Advanced web search | • Configurable search depth<br>• Result filtering<br>• Answer generation<br>• Topic-specific search |
| 📧 **Send Email** | Email sending capabilities | • Rich text support<br>• Attachment handling<br>• Template support |

## Advanced Features

### Output Schema Filtering

xpander.ai provides advanced [output schema filtering](https://docs.xpander.ai/user-guide/backend-configuration/connectors#tool-scheme-advanced-tab) that allows you to:

- **Reduce token usage** by removing unnecessary data
- **Remove PII** and sensitive information
- **Focus AI attention** on relevant response parts
- **Prevent data exposure** of irrelevant fields

### Tool Dependencies

Configure tool execution order in the xpander.ai platform:
- Set dependencies between tools
- Ensure proper workflow execution
- Create complex multi-step processes

## Project Structure

```
langchain/
├── xpander_langchain_example.ipynb  # Main example notebook
├── .env.example                     # Environment template
├── README.md                        # This file
└── requirements.txt                 # Python dependencies (optional)
```

## Customization

### Adding More Tools

1. Go to your xpander.ai agent configuration
2. Browse the tool library (2000+ available tools)
3. Add tools to your agent
4. They'll automatically be available in your LangChain agent

### Modifying Output Filtering

1. Access your tool configuration in xpander.ai
2. Navigate to the "Output Schema" tab
3. Configure which fields to include/exclude
4. Save your changes

### Changing the LLM

```python
# Use different OpenAI models
llm = ChatOpenAI(model="gpt-4", temperature=0.7)

# Or use other providers supported by LangChain
from langchain_anthropic import ChatAnthropic
llm = ChatAnthropic(model="claude-3-sonnet-20240229")
```

## Troubleshooting

### Common Issues

**Missing Environment Variables**
```
KeyError: Missing required environment variable: XPANDER_API_KEY
```
→ Ensure all required variables are set in your `.env` file

**Tool Call Errors**
```
Error: 2 validation errors for TavilySearchService...
```
→ Check your tool configuration in xpander.ai platform

**Authentication Errors**
```
401 Unauthorized
```
→ Verify your API keys are correct and have proper permissions

### Getting Help

- 📚 **Documentation**: [docs.xpander.ai](https://docs.xpander.ai)
- 💬 **Discord Community**: [Join our Discord](https://discord.gg/CUcp4WWh5g)
- 🐛 **Issues**: Report bugs in the GitHub repository
- ✉️ **Support**: Contact support through the xpander.ai platform

## Related Examples

Explore more framework integrations:

- [Agno Framework Example](../agno)
- [CrewAI Integration](../crewai)
- [OpenAI Assistant Example](../openai)

## License

MIT License - see the main repository for details.

---

**Ready to build production-grade AI agents?** [Start with xpander.ai](https://app.xpander.ai) 🚀
