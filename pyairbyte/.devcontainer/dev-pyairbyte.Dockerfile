FROM python:3.11.11-slim

# Useful Tools
# RUN apt-get update && apt-get install -y git curl nano

COPY requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt

# Create non root user for VSCode
ARG USERNAME=vscode
RUN useradd -m $USERNAME
WORKDIR /workspace
USER $USERNAME