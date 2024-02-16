#!/bin/bash

EXPIRED_TOKEN=$(az ad signed-in-user show --query 'id' -o tsv || true)

if [[ -z "$EXPIRED_TOKEN" ]]; then
    az login -o none
fi

if [[ -z "${AZURE_SUBSCRIPTION_ID:-}" ]]; then
    ACCOUNT=$(az account show --query '[id,name]')
    echo "You can set the \`AZURE_SUBSCRIPTION_ID\` environment variable with \`azd env set AZURE_SUBSCRIPTION_ID\`."
    echo $ACCOUNT
    
    read -r -p "Do you want to use the above subscription? (Y/n) " response
    response=${response:-Y}
    case "$response" in
        [yY][eE][sS]|[yY]) 
            ;;
        *)
            echo "Listing available subscriptions..."
            SUBSCRIPTIONS=$(az account list --query 'sort_by([], &name)' --output json)
            echo "Available subscriptions:"
            echo "$SUBSCRIPTIONS" | jq -r '.[] | [.name, .id] | @tsv' | column -t -s $'\t'
            read -r -p "Enter the name or ID of the subscription you want to use: " subscription_input
            AZURE_SUBSCRIPTION_ID=$(echo "$SUBSCRIPTIONS" | jq -r --arg input "$subscription_input" '.[] | select(.name==$input or .id==$input) | .id')
            if [[ -n "$AZURE_SUBSCRIPTION_ID" ]]; then
                echo "Setting active subscription to: $AZURE_SUBSCRIPTION_ID"
                az account set -s $AZURE_SUBSCRIPTION_ID
            else
                echo "Subscription not found. Please enter a valid subscription name or ID."
                exit 1
            fi
            ;;
        *)
            echo "Use the \`az account set\` command to set the subscription you'd like to use and re-run this script."
            exit 0
            ;;
    esac
else
    echo "Found AZURE_SUBSCRIPTION_ID environment variable. Setting active subscription to: $AZURE_SUBSCRIPTION_ID"
    az account set -s $AZURE_SUBSCRIPTION_ID
fi

# Convert WORKSPACE to lowercase and trim any whitespace
WORKSPACE=$(echo "${WORKSPACE:-default}" | tr '[:upper:]' '[:lower:]' | xargs)

# Continue with the rest of the script based on WORKSPACE value
if [ "$WORKSPACE" = "default" ]; then
    # Define the file path
    TF_DIR="infra/tfstate"
    
    # Set TF_VAR_location to the value of AZURE_LOCATION
    export TF_VAR_location=$AZURE_LOCATION
    
    # Set TF_VAR_environment_name to the value of AZURE_ENV_NAME
    export TF_VAR_environment_name=$AZURE_ENV_NAME
    
    # Initialize and apply Terraform configuration
    terraform -chdir="$TF_DIR" init
    terraform -chdir="$TF_DIR" apply -auto-approve
    
    # Add a delay to ensure that the service is up and running
    echo "Waiting for the service to be available..."
    sleep 30
    
    # Capture the outputs
    RS_STORAGE_ACCOUNT=$(terraform -chdir="$TF_DIR" output -raw RS_STORAGE_ACCOUNT)
    RS_CONTAINER_NAME=$(terraform -chdir="$TF_DIR" output -raw RS_CONTAINER_NAME)
    RS_RESOURCE_GROUP=$(terraform -chdir="$TF_DIR" output -raw RS_RESOURCE_GROUP)
    
    # Set the environment variables
    azd env set RS_STORAGE_ACCOUNT "$RS_STORAGE_ACCOUNT"
    azd env set RS_CONTAINER_NAME "$RS_CONTAINER_NAME"
    azd env set RS_RESOURCE_GROUP "$RS_RESOURCE_GROUP"
fi


# Configure the TF workspace for GH Action runs
TF_WORKSPACE_DIR="${GITHUB_WORKSPACE:+$GITHUB_WORKSPACE/}.azure/${AZURE_ENV_NAME}/infra/.terraform"

# Create the directory if it doesn't exist
mkdir -p "$TF_WORKSPACE_DIR"

# Use the variable with the terraform command
terraform -chdir="$TF_WORKSPACE_DIR" workspace select -or-create "$WORKSPACE"

