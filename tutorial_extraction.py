# Import necessary libraries
from datasets import load_dataset
from llama_index import Document, GPTVectorStoreIndex, StorageContext, ServiceContext
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.vector_stores import PineconeVectorStore
import openai
import os

# Install required packages (Uncomment when running in a fresh environment)
# !pip install -qU llama-index==0.9.29 datasets==2.16.1 pinecone-client==3.0.0 openai==1.7.1 transformers==4.36.2

# Define a more extensive knowledge base for demonstration
knowledge_base = {
    "encoded_question_1": "step1: open youtube; step2: search for 'fireship'; step3: click on the 'Videos' tab; step4: sort by date to find the newest video",
    "encoded_question_2": "step1: open google; step2: search for 'weather today'; step3: click on the first result to see detailed forecast",
    # Add more examples as needed
}

# Function to encode questions using OpenAI's text-davinci-003
def encode_question(question_text):
    openai.api_key = '<your_openai_api_key>'
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=question_text,
        max_tokens=50,
        stop=["\n"]
    )
    encoded_question = response.choices[0].text.strip()
    return encoded_question

# Initialize Pinecone
os.environ['PINECONE_API_KEY'] = '<your Pinecone API key>'
pc = Pinecone(api_key=os.getenv('PINECONE_API_KEY'))

index_name = 'llama-index-intro'
existing_indexes = [i.get('name') for i in pc.list_indexes()]

if index_name not in existing_indexes:
    pc.create_index(
        name=index_name,
        dimension=1536,
        metric='cosine',
        spec=ServerlessSpec(cloud='aws', region='us-west-2')
    )

pinecone_index = pc.Index(index_name)
vector_store = PineconeVectorStore(pinecone_index=pinecone_index)

# Embedding and service context setup
embed_model = OpenAIEmbedding(model='text-embedding-ada-002', embed_batch_size=100)
service_context = ServiceContext.from_defaults(embed_model=embed_model)

# Example query process
def query_process(query):
    encoded_query = encode_question(query)  # Encode the query
    steps = knowledge_base.get(encoded_query, "No steps found for the given query.")  # Retrieve steps from the knowledge base
    return steps

# Example query
query = "How to find the newest video from fireship on YouTube?"
steps = query_process(query)
print(steps)

# Clean up resources
pc.delete_index(index_name)
