# Use Alpine-based Python image
FROM python:3.12-alpine AS builder

# Set environment vars for venv
ENV VIRTUAL_ENV=/venv
ENV PATH="$VIRTUAL_ENV/bin:$PATH"
ENV PYTHONUNBUFFERED=1

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
    nodejs

# Create and activate virtualenv
RUN python3 -m venv $VIRTUAL_ENV

# Copy app files
COPY . .

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Run your main.py script (adjust path if needed)
CMD ["python", "xpander_handler.py"]
