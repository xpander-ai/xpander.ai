FROM python:3.12-slim AS builder

# Set working directory
WORKDIR /usr/src/app

# Install minimal dependencies without GUI packages
# Split into two RUN commands to avoid dependency conflicts
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    gcc \
    g++ \
    make \
    python3-dev \
    git \
    ca-certificates \
    build-essential \
    pkg-config \
    libssl-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install Node.js from NodeSource to avoid GUI dependencies
RUN curl -fsSL https://deb.nodesource.com/setup_lts.x | bash - \
    && apt-get install -y --no-install-recommends nodejs \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copy app files
COPY . .

# Create and activate virtualenv
RUN python3 -m venv .venv

# Add virtual environment to PATH
ENV PATH="/usr/src/app/.venv/bin:$PATH"

# Install using make install (handles agno conflict automatically)
RUN pip install --no-cache-dir --upgrade pip && \
    make install

# Run the xpander handler
CMD ["python", "xpander_handler.py"]
