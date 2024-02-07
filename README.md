# hello-ai

#### Setup
1. Fork the repo to your own account, include ALL branches.
1. Create a new Codespace.
1. Open in VS Code Desktop (via File menu).

#### Login
1. Run `azd auth login`
1. AZ Login `az login --scope https://graph.microsoft.com/.default`
   1. AZ login from within **Codespaces on Web** (due to this issue: https://github.com/Azure/azure-cli/issues/20315)
      - Login. It will fail. Copy the "localhost" URL from the failed redirect.
      - In Codespaces, open a new terminal.
      - Run `curl {the url you copied earlier}`
      - Close that terminal.
      - Go back to other terminal where you ran `az login`
      - It should show you your subscriptions.
      - Continue to next step
1. Run `az account set -n {sub}` to set right subscription.

#### Provision
1. Run `azd up` to provision only the Azure AI service. Choose "east us 2" region.

#### Run Locally
1. Hit F5
1. Go to https://localhost:3100 and view the quote

### Provision all resources to Azure

1. Run `azd env set WORKSPACE azure`
1. Run `azd up`. This will provision all Azure resources (AKS, Service Bus, etc)
1. Open API IP, which will be outputted to the terminal.

### Setup GitHub Action

1. Run `azd pipeline config`
1. Complete all the prompts
1. View the actions either in VS Code `GitHub Actions` extension or on GitHub.com