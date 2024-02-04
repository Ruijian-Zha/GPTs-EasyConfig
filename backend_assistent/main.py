
from dotenv import load_dotenv
import os
import json
import asyncio
from googleapiclient.discovery import build
from requests.exceptions import RequestException
import requests
from bs4 import BeautifulSoup
import urllib.robotparser
from openai import AsyncOpenAI
from .google_searcher import GoogleSearcher
from .openai_tools import OpenAITools

# Load the .env file where your DISCORD_TOKEN is stored
load_dotenv(override=True)

openai_api_key = os.getenv("OPENAI_API_KEY")
google_api_key = os.getenv("GOOGLE_API_KEY")
google_cse_id = os.getenv("GOOGLE_CSE_ID")

openai_client = AsyncOpenAI(api_key=openai_api_key)

sys_prompt = """"
You are an AI Assistant. You can assist with web navigation and search tasks.

## Tool:
- **Google Search:** Perform a Google search when you believe web searching is beneficial complete the task. 
"""

# The rest of the code can remain in this file or be refactored further as needed.
async def main():
    # Instantiate the OpenAITools class with the OpenAI client
    openai_tools = OpenAITools(openai_client)
    chatid_to_openai_thread_map = {}

    assistant = await openai_tools.openai_client.beta.assistants.create(
        name="WebAgent-Agent2.ai",
        instructions=sys_prompt,
        tools=[{
            "type": "function",
            "function": {
                "name": "google_search",
                "description": "Perform a Google search",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "query": {"type": "string", "description": "The search query to use. For example: 'Openai technical details'"},
                    },
                    "required": ["query"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "go_to_url",
                "description": "Navigate to a specified URL",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "url": {"type": "string", "description": "The URL to navigate to."}                    },
                    "required": ["url"]
                }
            }
        }
        ],
        model="gpt-4-1106-preview"
    )

    ASSISTANT_ID = assistant.id
    print(f"Assistant ID: {ASSISTANT_ID}")

    thread = await openai_tools.openai_client.beta.threads.create()  # Await the creation of the thread

    while True:
        user_input = input("User >> ")
        run = await openai_tools.submit_message(ASSISTANT_ID, thread, user_input)  # Await the submission of the message
        run = await openai_tools.wait_on_run(run, thread)  # Await the run status
        if run.status == 'failed':
            run = await openai_tools.submit_message(ASSISTANT_ID, thread, user_input)  # Await the resubmission of the message
            run = await openai_tools.wait_on_run(run, thread)  # Await the run status
        if run.status == 'requires_action':
            is_web_search = True
            while run.status == 'requires_action':
                run = await openai_tools.submit_tool_outputs(thread.id, run.id, run.required_action.submit_tool_outputs.tool_calls)  # Await the tool outputs submission
                run = await openai_tools.wait_on_run(run, thread)  # Await the run status

        response, user_message_id = await openai_tools.get_response(thread)  # Await the response retrieval

# This is the standard boilerplate that calls the main() function.
if __name__ == "__main__":
    asyncio.run(main())