#!/bin/bash

# Convert WORKSPACE to lowercase and trim any whitespace
WORKSPACE=$(echo "${WORKSPACE:-default}" | tr '[:upper:]' '[:lower:]' | xargs)

# Continue with the rest of the script based on WORKSPACE value and FORCE_TERRAFORM_REMOTE_STATE_CREATION condition
if [ "$WORKSPACE" = "default" ] && { [ -z "$FORCE_TERRAFORM_REMOTE_STATE_CREATION" ] || [ "$FORCE_TERRAFORM_REMOTE_STATE_CREATION" = "true" ]; }; then
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
    
    # Set the environment variables using the outputs
    azd env set RS_STORAGE_ACCOUNT "$RS_STORAGE_ACCOUNT"
    azd env set RS_CONTAINER_NAME "$RS_CONTAINER_NAME"
    azd env set RS_RESOURCE_GROUP "$RS_RESOURCE_GROUP"

    # Set FORCE_TERRAFORM_REMOTE_STATE_CREATION to false at the end of the block
    azd env set FORCE_TERRAFORM_REMOTE_STATE_CREATION "false"
fi

# Configure the TF workspace for GH Action runs
TF_WORKSPACE_DIR="${GITHUB_WORKSPACE:+$GITHUB_WORKSPACE/}.azure/${AZURE_ENV_NAME}/infra/.terraform"

# Create the directory if it doesn't exist
mkdir -p "$TF_WORKSPACE_DIR"

# Use the variable with the terraform command
terraform -chdir="$TF_WORKSPACE_DIR" workspace select -or-create "$WORKSPACE"

