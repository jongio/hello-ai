 #!/bin/sh

while IFS='=' read -r key value; do
    value=$(echo "$value" | sed 's/^"//' | sed 's/"$//')
    export "$key=$value"
done <<EOF
$(azd env get-values)
EOF


# Define the chat messages
CHAT_MESSAGES='{"messages":[{"role": "system", "content": "You are a helpful assistant."},{"role": "user", "content": "Does Azure OpenAI support customer managed keys?"},{"role": "assistant", "content": "Yes, customer managed keys are supported by Azure OpenAI."},{"role": "user", "content": "Do other Azure AI services support this too?"}]}'

# Define the chat endpoint
CHAT_ENDPOINT="${AZURE_OPENAI_ENDPOINT}openai/deployments/${AZURE_OPENAI_MODEL_NAME}/chat/completions?api-version=2023-05-15"
echo "AI Endpoint: ${AZURE_OPENAI_ENDPOINT}"
echo "REST Endpoint: ${CHAT_ENDPOINT}"

# Output the user messages
echo "==========User Messages=========="
echo "${CHAT_MESSAGES}" | jq -r '.messages[] | select(.role == "user") | .content'

# Make the curl request and output the assistant's reply
echo "==========AI Response=========="
curl -s ${CHAT_ENDPOINT} \
  -H "Content-Type: application/json" \
  -H "api-key: ${AZURE_OPENAI_API_KEY}" \
  -d "${CHAT_MESSAGES}" | jq -r '"Model: \(.model)\nMessage ID: \(.id)\nAssistant Reply: \(.choices[0].message.content)"'
