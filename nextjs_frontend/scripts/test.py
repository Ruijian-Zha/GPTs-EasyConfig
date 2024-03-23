import psycopg2
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Define connection parameters using environment variables
params = {
    'dbname': os.getenv('POSTGRES_DATABASE'),
    'user': os.getenv('POSTGRES_USER'),
    'password': os.getenv('POSTGRES_PASSWORD'),
    'host': os.getenv('POSTGRES_HOST'),
    'port': 5432,  # Default PostgreSQL port
    'sslmode': 'require'  # This is typically required for hosted PostgreSQL
}

# Connect to the PostgreSQL server
conn = psycopg2.connect(**params)

# Create a cursor
cur = conn.cursor()

#---------------------------------

# SQL command to update the URL for the entry with ID 0
update_query = """
UPDATE url_table SET url = 'https://01.ai' WHERE id = 0;
"""

# update_query = """
# UPDATE url_table SET url = 'https://huggingface.co/' WHERE id = 0;
# """

# Execute the update query
cur.execute(update_query)
#---------------------------------

conn.commit()

# Close the cursor and connection
cur.close()
conn.close()