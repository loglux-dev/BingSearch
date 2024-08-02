# Bing News Scraper

This repository contains a Python script that uses the Playwright library to scrape news articles from Bing News based on a specified query. The script is designed to be asynchronous and efficiently handles multiple pages of news results through automated scrolling.

## Features

- **Asynchronous Scraping**: Utilizes the `asyncio` library and Playwright's asynchronous API to perform non-blocking operations.
- **Automated Scrolling**: Automatically scrolls through Bing News search results to load more articles.
- **Data Extraction**: Extracts headlines, URLs, publication dates, and snippets for each news article.
- **Duplicate Filtering**: Ensures that only unique articles are added to the results list.

## Usage

To use the script, ensure you have Python 3.7+ installed along with the required dependencies. You can install dependencies using pip:

```bash
pip install playwright
```

Then, install the browser binaries needed by Playwright:
            
    ```bash
    python -m playwright install
    ```
## Running the Script
```bash
python -m asyncio get_bing_news.py
```
```python
query = '"google"+"cloud"'
asyncio.run(fetch_bing_news(query=query, max_scrolls=20, scroll_pause=2000))
```

- **query**: The search query to fetch news articles (use URL-encoded format for special characters).
- **max_scrolls**: Maximum number of times the page will be scrolled to load additional articles.
- **scroll_pause**: Time in milliseconds to wait after each scroll to allow new articles to load.

## Sample Output
```bash
Headline: Liquid C2 brings Google Cloud to Africa
URL: https://www.msn.com/en-us/travel/news/liquid-c2-brings-google-cloud-to-africa/ar-BB1nYnzr?ocid=BingNewsVerp
Date: 10/06/2024
Snippet: Liquid C2 has become the first Google Cloud Interconnect provider on the continent. This strategic partnership with global hyperscaler Google Cloud adds significant capacity to the cloud solutions ...

Headline: Apple’s Spending on Google Cloud Storage On Track to Soar 50% This Year
URL: https://www.theinformation.com/articles/apples-spending-on-google-cloud-storage-on-track-to-soar-50-this-year
Date: 29/06/2021
Snippet: Apple executives have taken swipes at Google in the past over its privacy practices. But the iPhone maker trusts Google enough so that over the past year it has dramatically increased the amount of ...
```
License
This project is licensed under the MIT License. See the LICENSE file for details.