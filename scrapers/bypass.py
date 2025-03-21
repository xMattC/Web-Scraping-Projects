import requests

# Target URL for testing
URL = "https://unsplash.com/s/photos/python"


def test_requests(url: str, agents: list):
    """
    Sends GET requests to the specified URL using different user agents.

    Parameters:
    url (str): The target URL to send requests to.
    agents (list): A list of user-agent strings to simulate different browsers.
    """
    for i, agent in enumerate(agents):
        # Send a GET request with a custom User-Agent header
        data_request = requests.get(url, headers={'User-Agent': agent})

        # Print request information
        print(f'Agent {i}:')
        print(f"Status Code: {data_request.status_code}")  # Display HTTP response status
        print(f"Headers: {data_request.request.headers}")  # Show request headers used


if __name__ == "__main__":
    # List of common User-Agent strings to simulate different browsers and devices
    # Source: https://techblog.willshouse.com/2012/01/03/most-common-user-agents/
    user_agents = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:135.0) Gecko/20100101 Firefox/135.0',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:136.0) Gecko/20100101 Firefox/136.0',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36 Edg/133.0.0.0',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36',
        'Mozilla/5.0 (X11; Linux x86_64; rv:135.0) Gecko/20100101 Firefox/135.0',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.3 Safari/605.1.15',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36'
    ]

    # Call function to send requests with different user agents
    test_requests(URL, user_agents)
