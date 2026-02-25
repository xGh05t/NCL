FROM python:3.11-slim

WORKDIR /opt

# Install dependencies
RUN apt-get update && \
    apt-get install -y git wget unzip build-essential && \
    rm -rf /var/lib/apt/lists/*

# Clone Volatility 3 (Version 2.26.2)
RUN git clone --branch v2.26.2 https://github.com/volatilityfoundation/volatility3.git

# Install Volatility 3
RUN cd volatility3 && pip install .

ENTRYPOINT ["vol"]
