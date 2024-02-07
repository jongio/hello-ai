#!/bin/bash

# Convert WORKSPACE to lowercase and trim any whitespace
WORKSPACE=$(echo "${WORKSPACE}" | tr '[:upper:]' '[:lower:]' | xargs)

# Check if WORKSPACE is set to "azure"
if [ "$WORKSPACE" = "azure" ]; then
    # Add a delay to ensure that the service is up and running
    echo "Waiting for the service to be available..."
    sleep 30
    
    # Check if AZD_PIPELINE_CONFIG_PROMPT is not set or is true
    if [ -z "${AZD_PIPELINE_CONFIG_PROMPT}" ] || [ "${AZD_PIPELINE_CONFIG_PROMPT}" = "true" ]; then
        
        echo "======================================================"
        echo "                     Github Action Setup                 "
        echo "======================================================"
        
        # Ask the user a question and get their response
        read -p "Do you want to configure a GitHub action to automatically deploy this repo to Azure when you push code changes? (Y/n) " response

        # Default response is "N"
        response=${response:-Y}

        # Check the response
        if [[ "$response" =~ ^[Yy]$ ]]; then
            echo "Configuring GitHub Action..."
            azd pipeline config
            # Set AZD_GH_ACTION_PROMPT to false
            azd env set AZD_PIPELINE_CONFIG_PROMPT false
        fi
    fi

    echo "Retrieving the external IP address of the service"
    echo "======================================================"
    echo " Website IP Address                 "
    echo "======================================================"
    API_IP=$(kubectl get svc api -o=jsonpath='{.status.loadBalancer.ingress[0].ip}')
    echo "API IP: http://$API_IP"
fi

azd env get-values > .env

# Retrieve the internalId of the Cognitive Services account
INTERNAL_ID=$(az cognitiveservices account show \
    --name ${AZURE_OPENAI_NAME} \
    -g ${AZURE_RESOURCE_GROUP} \
--query "properties.internalId" -o tsv)

# Construct the URL
COGNITIVE_SERVICE_URL="https://oai.azure.com/portal/${INTERNAL_ID}?tenantid=${AZURE_TENANT_ID}"

# Display OpenAI Endpoint and other details
echo "======================================================"
echo " AI Configuration                 "
echo "======================================================"
echo "    OpenAI Endpoint: ${AZURE_OPENAI_ENDPOINT}                    "
echo "    SKU Name: S0                             "
echo "    AI Model Name: ${AZURE_OPENAI_MODEL_NAME}                    "
echo "    Model Version: 0613                    "
echo "    Model Capacity: 120                "
echo "    Azure Portal Link:                                 "
echo "    https://ms.portal.azure.com/#@microsoft.onmicrosoft.com/resource/subscriptions/${AZURE_SUBSCRIPTION_ID}/resourceGroups/${AZURE_RESOURCE_GROUP}/providers/Microsoft.CognitiveServices/accounts/${AZURE_OPENAI_NAME}/overview"
echo "    Azure OpenAI Studio: ${COGNITIVE_SERVICE_URL}    "
echo ""
echo "======================================================"
echo " AI Test                 "
echo "======================================================"
echo " You can run the following to test the AI Service: "
echo "      ./tests/test-ai.sh"
echo ""
echo "======================================================"
echo " AI Key                 "
echo "======================================================"
echo " The Azure OpenAI Key is stored in the .env file in the root of this repo.  "
echo ""
echo " You can also find the key by running this following command: "
echo ""
echo "    azd env get-values"