ARG IMAGE=bullseye
FROM --platform=amd64 mcr.microsoft.com/devcontainers/${IMAGE}
RUN export DEBIAN_FRONTEND=noninteractive \
     && apt-get update && apt-get install -y xdg-utils \
     && apt-get clean -y && rm -rf /var/lib/apt/lists/*
RUN curl -fsSL https://azuresdkreleasepreview.blob.core.windows.net/azd/standalone/pr/3274/install-azd.sh | bash -s -- --base-url https://azuresdkreleasepreview.blob.core.windows.net/azd/standalone/pr/3274 --version '' --verbose --skip-verify