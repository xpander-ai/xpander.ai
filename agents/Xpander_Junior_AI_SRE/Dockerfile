# Use Alpine-based Python image
FROM python:3.12-alpine AS builder

# Set working directory
WORKDIR /usr/src/app

# Install dependencies
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
    npm \
    rust \
    cargo \
    git \
    nodejs \
    ca-certificates
# Download the latest installer
ADD https://astral.sh/uv/install.sh /uv-installer.sh

ENV PATH="/root/.local/bin/:$PATH"

# Run the installer then remove it
RUN sh /uv-installer.sh && rm /uv-installer.sh

# Create and activate virtualenv
RUN uv venv

# Copy app files
COPY . .

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Run your main.py script (adjust path if needed)
CMD ["python", "xpander_handler.py"]
