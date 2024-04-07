import os
from dotenv import load_dotenv
from openai import AzureOpenAI
from flask import jsonify

# Load environment variables
load_dotenv()


async def generate_openai_completion(user_query):
    # Azure OpenAI configuration
    api_key = os.environ["AZURE_OPENAI_API_KEY"]
    deployment_name = os.environ["DEPLOYMENT_NAME"]
    api_version = os.environ["API_VERSION_AZURE"]
    azure_endpoint = "https://pr-tech-fair-aoai.openai.azure.com/"

    # Search service configuration
    search_endpoint = "https://pr-tech-fair-acs.search.windows.net"
    search_key = os.environ["SEARCH_KEY"]
    search_index = os.environ["SEARCH_INDEX"]

    client = AzureOpenAI(
        base_url = f"{azure_endpoint}/openai/deployments/{deployment_name}/extensions",
        api_key = api_key,
        api_version = api_version,
    )

    try:
        chat_completions_options = {
            "model": deployment_name,
            "messages": [
                {"role": "system", "content": "You are an assistant."},
                {"role": "assistant", "content": "Respond in Spanish."},
                {"role": "user", "content": user_query}
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
        print(response)

        # response.model_dump_json(indent=2)

        return ({"completion_response": response.choices[0].messages[1]['content']})

    except Exception as e:
        return jsonify({"error": str(e)}), 500