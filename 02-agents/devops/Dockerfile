# Use Debian-based Python so torch wheels resolve
FROM python:3.12-slim

WORKDIR /usr/src/app

# Base OS deps
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl ca-certificates build-essential git \
 && rm -rf /var/lib/apt/lists/*

# Install uv (which provides uvx) and put it on PATH
RUN curl -LsSf https://astral.sh/uv/install.sh | sh
ENV PATH="/root/.local/bin:${PATH}"
RUN ln -sf /root/.local/bin/uv /usr/local/bin/uv \
 && ln -sf /root/.local/bin/uvx /usr/local/bin/uvx

# Install Python deps
COPY requirements.txt .
RUN python -m pip install --upgrade pip \
 && pip install --no-cache-dir -r requirements.txt

# Copy app after deps for better caching
COPY . .

# Optional: pre-warm the MCP server so first boot does not resolve at runtime.
# Replace the package name if you use a different MCP server.
# This will fail fast at build time if torch cannot resolve, which is what we want.
RUN uvx --from awslabs-aws-api-mcp-server --help || true

# Run your app
CMD ["python", "xpander_handler.py"]

