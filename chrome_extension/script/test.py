import requests
import time

# Function to send a URL to the server with the specified action
def send_url(action, url):
    # Determine the endpoint based on the action
    if action == 'refresh':
        endpoint = 'http://localhost:3000/refresh-url'
    elif action == 'open':
        endpoint = 'http://localhost:3000/open-url'
    else:
        print("Invalid action specified. Use 'refresh' or 'open'.")
        return

    # The data to send (the URL you want to open or refresh in Chrome)
    data = {'url': url}

    # Send a POST request to the endpoint
    response = requests.post(endpoint, json=data)

    print(response.text)

# Example usage
send_url('refresh', 'https://agent2.ai/')  # To refresh the current tab with the specified URL
time.sleep(5)  # Wait for 5 seconds
send_url('open', 'https://bing.com/')  # To open a new tab with the specified URL