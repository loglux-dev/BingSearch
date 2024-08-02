import requests
from bs4 import BeautifulSoup
import time


def fetch_bing_news(query, pages=5, results_per_page=10):
    base_url = "https://www.bing.com/news/search"
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        )
    }

    all_news_results = []

    for page in range(pages):
        # Calculate the starting result index for pagination
        first_result = page * results_per_page

        # Set up the parameters for the GET request
        params = {
            "q": query,
            "first": first_result,
            "count": results_per_page
        }

        # Send a GET request to Bing News
        response = requests.get(base_url, headers=headers, params=params)

        # Check if the request was successful
        if response.status_code == 200:
            # Parse the HTML content using BeautifulSoup
            soup = BeautifulSoup(response.text, 'html.parser')

            # Find all news items on the page
            news_items = soup.select('div.news-card')

            for item in news_items:
                # Extract the headline text
                headline_tag = item.select_one('a.title')
                headline = headline_tag.get_text(strip=True) if headline_tag else 'No title'

                # Extract the URL
                url = headline_tag['href'] if headline_tag else 'No URL'

                # Append the result to the list
                all_news_results.append({"headline": headline, "url": url})

            print(f"Page {page + 1} results:")
            for news in all_news_results[-len(news_items):]:
                print(f"Headline: {news['headline']}")
                print(f"URL: {news['url']}\n")

            # Sleep to avoid sending too many requests in a short period
            time.sleep(2)
        else:
            print(f"Failed to fetch news for page {page + 1}, status code: {response.status_code}")
            break

    print("\nAll News Results:")
    for news in all_news_results:
        print(f"Headline: {news['headline']}")
        print(f"URL: {news['url']}\n")


# Run the function
fetch_bing_news(query='"google" "cloud"', pages=3)
