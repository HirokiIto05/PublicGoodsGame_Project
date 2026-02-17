FROM python:3.11-slim

# Install system tools
RUN apt-get update && apt-get install -y \
    git \
    curl \
    wget \
    gdebi-core \
    && rm -rf /var/lib/apt/lists/*

# Install Quarto (latest .deb)
ARG QUARTO_VERSION=1.8.26
RUN wget https://github.com/quarto-dev/quarto-cli/releases/download/v${QUARTO_VERSION}/quarto-${QUARTO_VERSION}-linux-amd64.tar.gz && \
    tar -xvzf quarto-${QUARTO_VERSION}-linux-amd64.tar.gz -C /opt && \
    ln -s /opt/quarto-${QUARTO_VERSION}/bin/quarto /usr/local/bin/quarto && \
    rm quarto-${QUARTO_VERSION}-linux-amd64.tar.gz


# Set working directory
WORKDIR /workspace

# Copy dependencies
COPY ./requirements.txt .

# Install Python deps
RUN pip install --no-cache-dir -r requirements.txt
