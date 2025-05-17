# Hello World Agent Example

This directory contains a simple example agent implementation using the xpander.ai SDK, demonstrating core functionalities of the platform.

## Overview

The Hello World agent is designed to showcase how to build a framework-agnostic AI agent with xpander.ai's backend-as-a-service infrastructure. This agent can:

- Process natural language inputs
- Generate text responses
- Create images based on prompts
- Execute multi-step reasoning
- Use both local and cloud-based tools

## Directory Structure

```
hello-world/
├── app.py                      # CLI entry point for the agent
├── my_agent.py                 # Main agent implementation
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

## Getting Started

### Prerequisites

- Python 3.8+
- xpander-sdk and xpander-utils
- An xpander.ai account with API keys

### Setup

1. Create a Python virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate  # On Windows, use: .venv\Scripts\activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

Example output:
```
Collecting xpander-sdk (from -r requirements.txt (line 1))
  Using cached xpander_sdk-1.54.3-py3-none-any.whl.metadata (12 kB)
Collecting xpander-utils (from -r requirements.txt (line 2))
  Using cached xpander_utils-0.0.101-py3-none-any.whl.metadata (4.4 kB)
Collecting openai (from -r requirements.txt (line 3))
  Downloading openai-1.79.0-py3-none-any.whl.metadata (25 kB)
# ... additional package installations ...
Successfully installed aiohappyeyeballs-2.6.1 aiohttp-3.11.18 aiosignal-1.3.2 aiosseclient-0.1.8 
annotated-types-0.7.0 anyio-4.9.0 asyncio-3.4.3 attrs-25.3.0 cattrs-24.1.3 certifi-2025.4.26 
# ... other successfully installed packages ...
```

3. Configure your agent:

Update the `xpander_config.json` file with your API key and agent ID, or create an agent with:

```bash
xpander login
xpander agent new
```

### Running the Agent

#### CLI Mode

Run the agent in interactive command-line mode:

```bash
python app.py
```

This starts a conversation with the agent where you can interact with it directly.

Example output:
```
2025-05-17 19:04:12.373 | INFO     | my_agent:chat:79 - 🧠 Adding task to a new thread
2025-05-17 19:04:17.333 | INFO     | my_agent:_agent_loop:114 - 🪄 Starting Agent Loop
2025-05-17 19:04:21.295 | INFO     | my_agent:_agent_loop:120 - --------------------------------------------
------------------------------------
2025-05-17 19:04:21.295 | INFO     | my_agent:_agent_loop:121 - 🔍 Step 1
2025-05-17 19:04:25.807 | INFO     | providers.llms.openai.async_client:invoke_model:87 - 🔄 Model response 
received in 4.00 s
2025-05-17 19:04:25.808 | INFO     | providers.llms.openai.async_client:invoke_model:93 - 🔄 Tool call function name: xpfinish-agent-execution-finished
2025-05-17 19:04:33.398 | INFO     | my_agent:_agent_loop:178 - ✅ xpfinish-agent-execution-finished
2025-05-17 19:04:33.399 | INFO     | my_agent:_agent_loop:180 - 🔢 Step 1 tokens used: 1232 (output: 138, input: 1094)
2025-05-17 19:04:34.837 | INFO     | my_agent:_agent_loop:186 - ✨ Execution duration: 17.50 s
2025-05-17 19:04:34.838 | INFO     | my_agent:_agent_loop:189 - 🔢 Total tokens used: 1232 (output: 138, input: 1094)
2025-05-17 19:04:35.299 | INFO     | my_agent:chat:83 - ----------------------------------------------------
----------------------------
2025-05-17 19:04:35.300 | INFO     | my_agent:chat:84 - 🤖 Agent response: Hello! I can help you with a variety of tasks, including:

- Generating images from text descriptions (AI art, concept visuals, etc.)
- Answering questions and providing information on a wide range of topics
- Assisting with writing, editing, and summarizing text
- Downloading and reading files from the web
- Helping with creative projects, brainstorming, and more

If you have a specific request or want to see an example, just let me know!
You: 
```

#### Event-Driven Mode

Run the agent in event-driven mode to handle events from the xpander.ai platform:

```bash
python xpander_handler.py
```

When running correctly, the agent will start and wait for incoming events from the xpander.ai platform. There won't be immediate output unless an event is received.

Note: Make sure to use python3 if your system doesn't recognize the python command:

```bash
python3 xpander_handler.py
```

## Usage Examples

### Generating Images

Since this agent is configured to generate images, you can ask it to create visuals based on your prompts. During a conversation with the agent, try sending a message like:

```
Generate an image of a mountain landscape at sunset
```

The agent will process your request, call the appropriate tools, and return a URL to the generated image, which it will format in Markdown for display:

```
2025-05-17 19:10:23.456 | INFO     | my_agent:chat:79 - 🧠 Adding task to existing thread: thread_12345
2025-05-17 19:10:24.789 | INFO     | my_agent:_agent_loop:114 - 🪄 Starting Agent Loop
// ... processing logs ...
2025-05-17 19:10:35.123 | INFO     | my_agent:chat:84 - 🤖 Agent response: I've created an image of a mountain landscape at sunset for you:

![Mountain landscape at sunset](https://image-url-example.com/generated-image.jpg)

The image shows majestic mountains with snow-capped peaks silhouetted against a vibrant sunset sky with orange, pink, and purple hues reflecting off clouds and a tranquil lake in the foreground.
```

### Reading Local Files

You can also ask the agent to read files from your filesystem using its local tools:

```
Can you read the contents of agent_instructions.json?
```

The agent will use the `read_file` tool to access and display the file contents.

## Agent Capabilities

The Hello World agent demonstrates several key capabilities:

- **Framework-Agnostic Design**: Built without tight coupling to any specific AI framework
- **Asynchronous Processing**: Utilizes Python's asyncio for non-blocking operations
- **Tool Integration**: Uses both local and cloud-based tools
- **Memory Management**: Maintains conversation context across interactions
- **Observability**: Logs detailed execution metrics and token usage
- **Multi-Step Reasoning**: Coordinates complex reasoning chains

## Local Tools

This agent includes two local tools:

1. `read_file`: Reads file contents from the local filesystem
2. `download_url_to_file`: Downloads content from a URL and saves it locally

## Customization

### Changing Instructions

Modify the `agent_instructions.json` file to change the agent's role, goals, and general instructions.

### Switching LLM Providers

By default, the agent uses OpenAI. To switch to a different provider:

```python
# In my_agent.py
llm_provider = LLMProvider.ANTHROPIC  # Or another supported provider

# During initialization
self.agent.select_llm_provider(llm_provider)
```

### Adding Custom Tools

Add new tools by extending the `local_tools.py` file with additional functions and tool declarations.

## Deployment

Deploy the agent to xpander.ai's managed infrastructure:

```bash
xpander deploy
```

Monitor the deployed agent's logs:

```bash
xpander logs
```

## Troubleshooting

- **Authentication Issues**: Verify your API key in `xpander_config.json`
- **Missing Dependencies**: Ensure all requirements are installed
- **Tool Execution Errors**: Check the logs for detailed error messages

## Additional Resources

- [xpander.ai Documentation](https://docs.xpander.ai)
- [SDK API Reference](https://docs.xpander.ai/api-reference/07-sdk)
- [Example Library](https://github.com/xpander-ai/xpander.ai/tree/main/examples) 

## Exploring the Code

To better understand how the agent works, here are the key files to examine:

1. **my_agent.py**: The core agent implementation that handles:
   - Initialization with xpander.ai SDK
   - The agent reasoning loop with `_agent_loop()`
   - Tool execution flow
   - Token usage tracking and metrics

2. **xpander_handler.py**: Event-driven architecture implementation showing:
   - How to register event handlers with the xpander platform
   - Processing incoming execution requests
   - Returning structured results

3. **tools/local_tools.py**: Example tool implementations with:
   - Function definitions
   - Tool schema declarations
   - Helper utilities for tool registration

The code is structured to demonstrate best practices for building AI agents with xpander.ai, including:

- Clean separation of concerns
- Asynchronous processing
- Structured error handling
- Detailed logging
- Modular tool implementation

When modifying the agent, start by examining these files to understand the execution flow before making changes. 