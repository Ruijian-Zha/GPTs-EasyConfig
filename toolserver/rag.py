import openai
import os
from dotenv import load_dotenv
from llama_index.core import Document, VectorStoreIndex

# Load environment variables from a .env file
load_dotenv()

# Retrieve OPENAI_API_KEY from environment variables
openai.api_key = os.getenv("OPENAI_API_KEY")

if openai.api_key is None:
    logging.error("OpenAI API key is not set in environment variables.")
    exit(1)

# Assuming you have your text data and corresponding metadata
text_list = [
    "This is a tutorial for YouTube video search, which is used for video finding tasks like finding the newest video about AI.",
    "A guide to using Google Maps for beginners, focusing on how to navigate and find specific locations efficiently.",
    "Exploring Spotify: A walkthrough on how to discover new music and create personalized playlists."
]
metadata_list = [
    {
        "task_id": "1", 
        "task_name": "youtube video search", 
        "steps": "1. Open youtube.com in your web browser; 2. Enter 'newest AI videos' in the search bar; 3. Press enter or click the search icon to find videos."
    },
    {
        "task_id": "2",
        "task_name": "google maps navigation",
        "steps": "1. Open maps.google.com in your web browser; 2. Enter the destination in the search bar; 3. Choose the mode of transportation; 4. Follow the highlighted route to reach your destination."
    },
    {
        "task_id": "3",
        "task_name": "spotify music discovery",
        "steps": "1. Open the Spotify app or website; 2. Use the search bar to find artists, albums, or playlists; 3. Follow artists or save albums to your library; 4. Explore the 'Made for You' section for personalized playlists."
    },
]

# Create Document objects with metadata
documents = [Document(text=text_list[i], metadata=metadata_list[i]) for i in range(len(text_list))]

# Create a vector store and index from documents
index = VectorStoreIndex.from_documents(documents)

# Set up the query engine
query_engine = index.as_query_engine()

# Perform a query
response = query_engine.query("how to find a certain youtube video?")

print(response)

# Displaying the query response with task details
uuid, details = next(iter(response.metadata.items()))
print(f"Task ID: {details['task_id']}, Task Name: {details['task_name']}, Steps: {details['steps']}")