
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

# Load the .env file where your DISCORD_TOKEN is stored
load_dotenv(override=True)

openai_api_key = os.getenv("OPENAI_API_KEY")
# openai_client = AsyncOpenAI(api_key=openai_api_key)
google_api_key = os.getenv("GOOGLE_API_KEY")
google_cse_id = os.getenv("GOOGLE_CSE_ID")


class GoogleSearcher:
    def __init__(self, api_key, cse_id):
        self.api_key = api_key
        self.cse_id = cse_id

    async def search(self, search_term, num_results=2, **kwargs):
        service = build("customsearch", "v1", developerKey=self.api_key)
        try:
            res = service.cse().list(q=search_term, cx=self.cse_id, num=num_results, **kwargs).execute()

            all_text = ""
            valid_websites_scraped = 0

            for item in res.get('items', []):
                url = item['link']
                print("Title:", item['title'])
                print("Link:", url)

                try:
                    if not self.is_scraping_allowed(url):
                        print(f"Scraping not allowed for {url}")
                        continue

                    page = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'}, timeout=5)
                    page.raise_for_status()  # Checks for HTTP errors
                    
                    soup = BeautifulSoup(page.content, "html.parser")
                    for script_or_style in soup(["script", "style"]):
                        script_or_style.decompose()

                    all_text += soup.get_text(separator=' ', strip=True) + "\n\n"
                    valid_websites_scraped += 1

                    if valid_websites_scraped >= 2:
                        break

                except RequestException as e:
                    print(f"Request failed for {url}: {e}")
                    continue

            return all_text
        except Exception as e:
            print(f"An error occurred during the Google search: {e}")
            return ""

    @staticmethod
    def is_scraping_allowed(url):
        try:
            rp = urllib.robotparser.RobotFileParser()
            rp.set_url(urllib.parse.urljoin(url, '/robots.txt'))
            rp.read()
            return rp.can_fetch("*", url)
        except Exception as e:
            print(f"Error checking robots.txt for {url}: {e}")
            return False