# Glibc-based Python so PyTorch wheels work
FROM python:3.12-slim AS runtime

ENV DEBIAN_FRONTEND=noninteractive \
    PIP_NO_CACHE_DIR=1 \
    UV_LINK_MODE=copy \
    PATH="/usr/src/app/.venv/bin:/root/.local/bin:${PATH}"

# System deps
RUN apt-get update && apt-get install -y --no-install-recommends \
    bash curl git ca-certificates \
    build-essential libffi-dev libssl-dev \
    rustc cargo \
    nodejs npm \
  && rm -rf /var/lib/apt/lists/*

# Install uv
RUN curl -fsSL https://astral.sh/uv/install.sh | sh

WORKDIR /usr/src/app
COPY . .

# Project venv
RUN python -m venv .venv

# Install Python deps.
# Ensure a CPU wheel for torch exists for cp312 on arm64/x64.
# The extra index is defensive and harmless if PyPI already satisfies it.
RUN pip install --upgrade pip \
 && pip install --only-binary=:all: --extra-index-url https://download.pytorch.org/whl/cpu "torch==2.8.0" \
 && pip install -r requirements.txt

# Pre-warm uvx cache for the MCP tool that depends on torch
# This prevents runtime resolution stalls or surprises
RUN uvx --from awslabs-aws-api-mcp-server aws-api-mcp --help || true

CMD ["python", "xpander_handler.py"]