# MCP Agno Example for AIQ Toolkit

Agno agent with MCP tools for Kubernetes assistance.

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
uv pip install -e .
```

Create `.env`:

```bash
AWS_ACCESS_KEY_ID=your-key
AWS_SECRET_ACCESS_KEY=your-secret
AWS_REGION=us-west-2
OPENAI_API_KEY=your-key
```

## Run

```bash
source .venv/bin/activate
export $(cat .env | grep -v '^#' | xargs)
aiq run --config_file workflow.yaml --input "What can you help me with?"
```

## Files

- `workflow.yaml` - AIQ config (LLM model, function registration)
- `mcp_agno_function.py` - Agent implementation
- `pyproject.toml` - Dependencies

## Notes

- Use `uv pip install`, not pip
- LLM model configured in workflow.yaml
- Agno framework, not LangChain