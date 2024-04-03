import os
from dotenv import load_dotenv
from openai import AzureOpenAI

load_dotenv() 

# Replace with your actual values
api_key = os.environ["AZURE_OPENAI_API_KEY"]
deployment_name = os.environ["DEPLOYMENT_NAME"]
api_version = os.environ["API_VERSION_AZURE"]
azure_endpoint = "https://pr-tech-fair-aoai.openai.azure.com/"

# Search service configuration (replace with your details)
search_endpoint = "https://pr-tech-fair-acs.search.windows.net"
search_key = os.environ["SEARCH_KEY"]
search_index = os.environ["SEARCH_INDEX"]

client = AzureOpenAI(
    #base_url = azure_endpoint,
    base_url = f"{azure_endpoint}/openai/deployments/{deployment_name}/extensions",
    api_key = api_key,
    api_version = api_version,
    #azure_ad_token_provider = token_provider,
)

# Define chat completion options
chat_completions_options = {
    "model": deployment_name,  # Use 'model' for non-Azure client
    "messages": [
        #{"role": "system", "content": "You are a chat assistant"},
        {"role": "user", "content": "What is the total population of students in Puerto Rico?"}
    ],
    "extra_body": {
        "dataSources": [
            {
                "type": "AzureCognitiveSearch",
                "parameters": {
                    "endpoint": search_endpoint,
                    "key": search_key,
                    "indexName": search_index,
                }
            }
        ]
    }
}

# Get chat completions
response = client.chat.completions.create(**chat_completions_options)
#print(response.model_dump_json(indent=2))
#print(type(response))
#print(response.choices[0])

print(response.choices[0].messages[1]['content'])
