import os
from dotenv import load_dotenv
from openai import AzureOpenAI

load_dotenv() 

# Replace with your actual values
api_version = os.environ["API_VERSION_AZURE"]
azure_endpoint = "https://pr-tech-fair-aoai.openai.azure.com/"
deployment_name = os.environ["DEPLOYMENT_NAME"]

# Search service configuration (replace with your details)
search_endpoint = "https://pr-tech-fair-acs.search.windows.net"
search_key = os.environ["SEARCH_KEY"]
search_index = os.environ["SEARCH_INDEX"]

'''# Entiendo que no es necesario
from azure.identity import DefaultAzureCredential, get_bearer_token_provider
token_provider = get_bearer_token_provider(DefaultAzureCredential(), 
                                           "https://cognitiveservices.azure.com/.default")'''

client = AzureOpenAI(
    api_version = api_version,
    azure_endpoint = azure_endpoint,
    #azure_ad_token_provider = token_provider,
)

# Define Azure chat extension options
# Not sure if this is the way
class AzureChatExtensionsOptions:
    def __init__(self, search_endpoint, search_key, search_index):
        self.search_endpoint = search_endpoint
        self.authentication = search_key
        self.index_name = search_index

# Instantiate Azure chat extension options
azure_chat_extensions_options = AzureChatExtensionsOptions(
    search_endpoint = search_endpoint,
    search_key = search_key,
    search_index = search_index
)

# Define chat completion options
chat_completions_options = {
    "model": deployment_name,  # Use 'model' for non-Azure clients
    "azure_extensions_options": {
        "extensions": [azure_chat_extensions_options]
    },
    "messages": [
        {"role": "system", "content": "You are a chat assistant"},
        {"role": "user", "content": "What is the total population of students in Puerto Rico?"}
    ],
    "extra_body": {
        "data_sources": [
            {
                "type": "azure_search",
                "parameters": {
                    "endpoint": search_endpoint,
                    "index_name": search_index,
                    "authentication": {
                        "type": "system_assigned_managed_identity"
                    }
                }
            }
        ]
    }
}

# Get chat completions
response = client.chat_completions.create(**chat_completions_options)

# Access response message
response_message = response.choices[0].message
print(f"[{response_message.role.upper()}] {response_message.content}")
print(response.model_dump_json(indent=2))










