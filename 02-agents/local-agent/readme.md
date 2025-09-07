# Local Agent

A completely local, open-source AI agent using **xpander.ai**, **Agno**, and **Ollama**.

## Features

- **Privacy-First**: All processing happens locally with open-source models
- **No External APIs**: Uses Ollama for local LLM runtime
- **Production Ready**: Docker containerization and cloud deployment
- **Multi-Source Tasks**: WebUI, Slack, API integration via xpander.ai backend

## Quick Start

```bash
# Install xpander.ai CLI
npm install -g xpander-cli

# Install Ollama
brew install ollama  # macOS
# curl -fsSL https://ollama.ai/install.sh | sh  # Linux

# Pull and start model
ollama pull gpt-oss:20b
ollama serve

# Create agent project  
xpander agent new --name "local-agent" --framework agno --folder .

# Set up environment
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Configuration

Configure your agent to use local Ollama models in `xpander_handler.py`:

```python
...
from agno.models.ollama import Ollama
...

agno_agent = Agent(**backend.get_args(override={
    'model': Ollama(id="gpt-oss:20b")
}))
```

## Usage

```bash
# Local development
python xpander_handler.py

# Docker deployment
docker build . -t local-agent
docker run --name local-agent -d \
  -e OLLAMA_HOST=http://host.docker.internal:11434 \
  --env-file .env \
  local-agent

# Test agent
xpander agent invoke "local-agent" "hi, are you there?"

# Deploy to cloud
xpander agent deploy
```

## Architecture

- **`@on_task`**: SSE event listener for tasks from WebUI, Slack, API
- **Ollama**: Local LLM runtime (gpt-oss:20b, llama3.2, mistral)
- **Xpander Backend**: Task routing, storage, tool management
- **Docker**: Containerized deployment

## Management

Access [app.xpander.ai](https://app.xpander.ai) for:

✅ Tool management and configuration  
✅ System prompts and agent settings  
✅ Usage metrics and monitoring  
✅ Multi-source task routing  
✅ Conversation history (Optional)

## Requirements

- Python 3.8+
- Ollama with local models
- Docker (optional)
- xpander.ai CLI