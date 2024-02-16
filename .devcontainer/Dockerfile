# Use a specific tag for the bullseye image to ensure reproducibility
ARG IMAGE=bullseye
FROM --platform=amd64 mcr.microsoft.com/devcontainers/${IMAGE}:latest

# Combine RUN instructions to reduce layers and use cleanup in the same layer as install to reduce image size
RUN export DEBIAN_FRONTEND=noninteractive && \
    apt-get update && \
    apt-get install -y xdg-utils && \
    # Clean up in the same layer to reduce the final image size
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* /var/cache/apt/archives/*

# Install Azure DevOps (azd) in a single RUN command to reduce layers, and avoid unnecessary verbose and skip-verify unless needed
RUN curl -fsSL https://azuresdkreleasepreview.blob.core.windows.net/azd/standalone/pr/3385/install-azd.sh | bash -s -- \
    --base-url https://azuresdkreleasepreview.blob.core.windows.net/azd/standalone/pr/3385 \
    --version ''
