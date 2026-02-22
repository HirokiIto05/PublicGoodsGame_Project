FROM python:3.11-slim

# Install system tools
RUN apt-get update && apt-get install -y \
    git \
    curl \
    wget \
    gdebi-core \
    && rm -rf /var/lib/apt/lists/*

# Install Quarto (auto-detect architecture)
ARG QUARTO_VERSION=1.8.26
RUN ARCH=$(uname -m) && \
    if [ "$ARCH" = "aarch64" ]; then QUARTO_ARCH="arm64"; \
    elif [ "$ARCH" = "x86_64" ]; then QUARTO_ARCH="amd64"; \
    else echo "Unsupported architecture: $ARCH" && exit 1; fi && \
    wget https://github.com/quarto-dev/quarto-cli/releases/download/v${QUARTO_VERSION}/quarto-${QUARTO_VERSION}-linux-${QUARTO_ARCH}.tar.gz && \
    tar -xvzf quarto-${QUARTO_VERSION}-linux-${QUARTO_ARCH}.tar.gz -C /opt && \
    ln -s /opt/quarto-${QUARTO_VERSION}/bin/quarto /usr/local/bin/quarto && \
    rm quarto-${QUARTO_VERSION}-linux-${QUARTO_ARCH}.tar.gz


# Set working directory
WORKDIR /workspace

# Copy dependencies
COPY ./requirements.txt .

# Install Python deps
RUN pip install --no-cache-dir -r requirements.txt

# Add alias for otree devserver
RUN echo 'alias otree-devserver="otree devserver 0.0.0.0:8000"' >> /root/.bashrc
