FROM ubuntu:22.04

# Avoid interactive prompts
ENV DEBIAN_FRONTEND=noninteractive

# Install required tools
RUN apt-get update && apt-get install -y \
    build-essential \
    linux-headers-$(uname -r) \
    clang-tidy \
    git \
    gcc-12 \
    make \
    python3 \
    python3-pip \
    wget \
    bc \
    cpio \
    kmod \
    flex \
    bison \
    gcc-12 \
    make \
    kmod \
    pkg-config \
    bc \
    flex \
    bison \
    libelf-dev \
    libssl-dev \
    linux-headers-$(uname -r)\
    && rm -rf /var/lib/apt/lists/*



# Get Linux kernel source scripts (for checkpatch.pl)
RUN git clone --depth=1 https://github.com/torvalds/linux.git /usr/src/linux && \
    ln -s /usr/src/linux/scripts/checkpatch.pl /usr/local/bin/checkpatch.pl

# Python packages (for scoring + CodeBLEU if you add later)
RUN pip install --no-cache-dir regex

# Set workspace
WORKDIR /workspace

