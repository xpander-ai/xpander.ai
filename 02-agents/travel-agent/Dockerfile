# Use Alpine-based Python image
FROM python:3.12-alpine AS builder

# Set working directory
WORKDIR /usr/src/app

# Install dependencies (including Node.js and npm directly)
RUN apk add --no-cache \
    curl \
    bash \
    gcc \
    g++ \
    libffi-dev \
    musl-dev \
    openssl-dev \
    make \
    python3-dev \
    rust \
    cargo \
    git \
    nodejs \
    npm \
    ca-certificates

# Copy app files
COPY . .

# Create and activate virtualenv
RUN python3 -m venv .venv

# Add virtual environment to PATH
ENV PATH="/usr/src/app/.venv/bin:$PATH"

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Run the xpander handler
CMD ["python", "xpander_handler.py"]
