import asyncio
from playwright.async_api import async_playwright

async def fetch_bing_news(query, max_scrolls=5):
    async with async_playwright() as p:
        # Launch the browser
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        # Navigate to Bing News search with the specified query
        await page.goto(f"https://www.bing.com/news/search?q={query}")

        # Store the results in a list
        news_results = []

        # Perform scrolling to load more results
        for scroll in range(max_scrolls):
            # Extract news headlines and URLs
            news_items = await page.query_selector_all('div.news-card')

            for item in news_items:
                headline_tag = await item.query_selector('a.title')
                headline = await headline_tag.inner_text() if headline_tag else 'No title'
                url = await headline_tag.get_attribute('href') if headline_tag else 'No URL'
                news_results.append({"headline": headline, "url": url})

            # Scroll down to load more results
            await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            await page.wait_for_timeout(2000)  # Wait for content to load

            print(f"Scroll {scroll + 1} results:")
            for news in news_results[-len(news_items):]:
                print(f"Headline: {news['headline']}")
                print(f"URL: {news['url']}\n")

        # Close the browser
        await browser.close()

    print("\nAll News Results:")
    for news in news_results:
        print(f"Headline: {news['headline']}")
        print(f"URL: {news['url']}\n")

# Run the async function
query = '"google"+"cloud"'
asyncio.run(fetch_bing_news(query=query, max_scrolls=5))
