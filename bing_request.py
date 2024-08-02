import requests
from bs4 import BeautifulSoup


def fetch_bing_news():
    # Define the URL with search query "Google Cloud"
    url = "https://www.bing.com/news/search?q=%22google%22+%22cloud%22&count=900"

    # Set up the headers to mimic a browser request
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        )
    }

    # Send a GET request to Bing News
    response = requests.get(url, headers=headers)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find all news items
        news_items = soup.select('div.news-card')

        # Store the results in a list
        news_results = []
        for item in news_items:
            # Extract the headline text
            headline_tag = item.select_one('a.title')
            headline = headline_tag.get_text(strip=True) if headline_tag else 'No title'

            # Extract the URL
            url = headline_tag['href'] if headline_tag else 'No URL'

            # Append the result to the list
            news_results.append({"headline": headline, "url": url})

        # Print the results
        for news in news_results:
            print(f"Headline: {news['headline']}")
            print(f"URL: {news['url']}\n")
    else:
        print(f"Failed to fetch news, status code: {response.status_code}")


# Run the function
fetch_bing_news()
