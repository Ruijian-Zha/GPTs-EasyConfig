import openai
import json
from duckduckgo_search import duckduckgo_search

openai.api_key = "EMPTY"
openai.api_base = "http://luigi.millennium.berkeley.edu:8000/v1"

# Example dummy function hard coded to return the same weather
# In production, this could be your backend API or an external API
def get_current_weather(location, unit="fahrenheit"):
    """Get the current weather in a given location"""
    weather_info = {
        "location": location,
        "temperature": "72",
        "unit": unit,
        "forecast": ["sunny", "windy"],
    }
    return json.dumps(weather_info)

def run_conversation():
    while True:
        user_input = input("User >> ")
        
        # Step 1: send the conversation and available functions to GPT
        messages = [{"role": "user", "content": user_input}]

        # Step 1: send the conversation and available functions to GPT
        # messages = [{"role": "user", "content": "What's the weather like in the two cities of Boston and San Francisco?"}]
        functions = [
            {
                "name": "get_current_weather",
                "description": "Get the current weather in a given location",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "location": {
                            "type": "string",
                            "description": "The city and state, e.g. San Francisco, CA",
                        },
                        "unit": {"type": "string", "enum": ["celsius", "fahrenheit"]},
                    },
                    "required": ["location"],
                },
            },
            {
                "name": "web_search",
                "description": "Perform a web search for a given query",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "query": {
                            "type": "string",
                            "description": "The search query string",
                        },
                    },
                    "required": ["query"],
                },
            }
        ]
        
        completion = openai.ChatCompletion.create(
            model='gorilla-openfunctions-v2',
            messages=messages,
            functions=functions,
            function_call="auto",
        )

        print("--------------------")
        print(f"Function call strings(s): {completion.choices[0].message.content}")
        print("--------------------")

        # Check if there is a function call
        function_call_data = completion.choices[0].message.function_call
        if function_call_data:
            print(f"OpenAI compatible `function_call`: {function_call_data}")
            # Ensure function_calls is a list
            function_calls = function_call_data if isinstance(function_call_data, list) else [function_call_data]

            # Iterate over the function calls and execute them
            for func_call in function_calls:
                func_name = func_call['name']
                arguments = func_call['arguments']
                if func_name == "get_current_weather":
                    # Call the function with the provided arguments
                    result = get_current_weather(**arguments)
                    print("--------------------")
                    print(f"Output of `{func_name}` with arguments {arguments}:")
                    print(result)
                    print("--------------------")
                elif func_name == "web_search":
                    # Call the duckduckgo_search function with the provided arguments
                    result = duckduckgo_search(arguments['query'])
                    print("--------------------")
                    print(f"Output of `{func_name}` with arguments {arguments}:")
                    print(result)
                    print("--------------------")
        else:
            print("No function calls to execute.")

run_conversation()