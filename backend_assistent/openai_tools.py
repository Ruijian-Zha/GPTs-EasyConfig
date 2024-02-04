
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
from .selenium_operations import SeleniumOperations

# Load the .env file where your DISCORD_TOKEN is stored
load_dotenv(override=True)

openai_api_key = os.getenv("OPENAI_API_KEY")
google_api_key = os.getenv("GOOGLE_API_KEY")
google_cse_id = os.getenv("GOOGLE_CSE_ID")


class OpenAITools:
    def __init__(self, openai_client):
        self.openai_client = AsyncOpenAI(api_key=openai_api_key)

    async def submit_message(self, assistant_id, thread, user_message):
        # Add the user's message to the thread
        message = await self.openai_client.beta.threads.messages.create(
            thread_id=thread.id, role="user", content=user_message
        )
        # Create a run to process the message and return it
        return await self.openai_client.beta.threads.runs.create(
            thread_id=thread.id, assistant_id=assistant_id,
        )

    async def submit_tool_outputs(self, thread_id, run_id, tools_to_call):
        tool_output_array = []
        expected_call_ids = {tool.id for tool in tools_to_call}
        actual_call_ids = set()

        for tool in tools_to_call:
            output = None
            tool_call_id = tool.id
            actual_call_ids.add(tool_call_id)
            function_name = tool.function.name
            function_args = tool.function.arguments

            if function_name == "google_search":
                try:
                    args = json.loads(function_args)
                    if "query" in args:
                        google_searcher = GoogleSearcher(google_api_key, google_cse_id)
                        output = await google_searcher.search(args["query"])  # Ensure google_search is awaited if it's an async function
                    else:
                        print("The 'query' parameter is missing in function arguments.")
                except json.JSONDecodeError as e:
                    print(f"JSON decoding error: {e}")
            
            elif function_name == "go_to_url":
                try:
                    args = json.loads(function_args)
                    if "url" in args:
                        # Initialize SeleniumOperations if it hasn't been already
                        if SeleniumOperations.driver is None:
                            SeleniumOperations()
                        
                        # Use the go_to_url method to navigate to the specified URL
                        SeleniumOperations().go_to_url(args["url"])
                        output = {"status": "success", "message": f"Navigated to {args['url']}"}
                    else:
                        print("The 'url' parameter is missing in function arguments.")
                except json.JSONDecodeError as e:
                    print(f"JSON decoding error: {e}")

            if output:
                tool_output_array.append({"tool_call_id": tool_call_id, "output": json.dumps(output)})
            else:
                print(f"No output generated for tool_call_id: {tool_call_id}")

        missing_call_ids = expected_call_ids - actual_call_ids
        if missing_call_ids:
            print(f"Missing outputs for call_ids: {missing_call_ids}")

        if not tool_output_array or len(tool_output_array) != len(expected_call_ids):
            print(f"Expected outputs for call_ids: {expected_call_ids}, but got outputs for call_ids: {[output['tool_call_id'] for output in tool_output_array]}")
            # Handle the case where no outputs are generated
            return None

        return await self.openai_client.beta.threads.runs.submit_tool_outputs(
            thread_id=thread_id,
            run_id=run_id,
            tool_outputs=tool_output_array
        )

    async def wait_on_run(self, run, thread): # Use discord_thread.typing() instead of message.channel.typing()
        while True:
            # Sleep for 1 second to avoid excessive API calls
            await asyncio.sleep(1)
            # Retrieve the updated run status
            run = await self.openai_client.beta.threads.runs.retrieve(
                thread_id=thread.id, run_id=run.id,
            )
            print(f"Current run status: {run.status}")
            if run.status in ['completed', 'failed', 'requires_action']:
                break  # Exit the while loop if the status is one of the specified

        return run  # Return the run after exiting the while loop

    async def get_response(self, thread):
        messages_response = await self.openai_client.beta.threads.messages.list(thread_id=thread.id, order="desc", limit=10)
        # Extract the list of messages from the response
        messages_data = dict(messages_response).get('data', [])
        # print(messages_data)
        # Check if messages_data is not empty and is a list
        if messages_data and isinstance(messages_data, list):
            # Find the latest assistant message
            assistant_message = next((msg for msg in messages_data if msg.role == 'assistant'), None)
            if assistant_message:
                # Assuming the message content is a list and the first item is the text content
                latest_message_text = assistant_message.content[0].text.value
                # Display the latest assistant message text with a dividing line
                print(f"------------------------------------------------\nLast Assistant Message: {latest_message_text}\n------------------------------------------------")
                return latest_message_text, assistant_message.id

        # If messages_data is empty or not structured as expected, handle the error
        print("No assistant messages in the thread or unexpected message structure.")
        return None, None
