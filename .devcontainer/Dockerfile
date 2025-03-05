# Use Ubuntu 22.04 as the base image
FROM ubuntu:22.04

# Update package list and install necessary tools and dependencies
RUN apt-get update && \
    apt-get install -y \
    sudo \
    git \
    curl \
    gnupg \
    make \
    build-essential \
    pkg-config \
    libzmq3-dev \
    libssl-dev \
    zlib1g-dev \
    libncurses5-dev \
    libgdbm-dev \
    libnss3-dev \
    libsqlite3-dev \
    libreadline-dev \
    libffi-dev \
    libbz2-dev



# Install Python 3 using apt
RUN sudo apt-get install -y python3 python3-pip

# Install uv
RUN curl -LsSf https://astral.sh/uv/install.sh | sh