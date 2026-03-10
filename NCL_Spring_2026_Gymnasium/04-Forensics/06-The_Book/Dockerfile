FROM python:3.11-slim-bookworm

WORKDIR /opt

# Install required system packages
RUN apt-get update && \
    apt-get install -y \
        git \
        build-essential \
        yara \
        binutils \
        file \
        curl \
    && rm -rf /var/lib/apt/lists/*

# Clone Volatility 3 (core)
RUN git clone --branch v2.26.2 \
    https://github.com/volatilityfoundation/volatility3.git

# Clone community plugins
RUN git clone https://github.com/volatilityfoundation/community3.git

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir \
        distorm3 \
        yara-python \
        capstone \
        pefile \
        pypykatz \
        impacket \
        pycryptodome \
        cryptography \
        construct \
        asn1crypto && \
    cd volatility3 && pip install --no-cache-dir .

# Create symbol directory
RUN mkdir -p /symbols
ENV VOLATILITY_SYMBOLS=/symbols

# Add community plugins to plugin path
ENV VOLATILITY_PLUGIN_DIRS=/opt/community3

ENTRYPOINT ["vol"]
