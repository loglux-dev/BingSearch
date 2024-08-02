import asyncio
from playwright.async_api import async_playwright

async def fetch_bing_news(query, max_scrolls=10, scroll_pause=3000):
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

            new_articles_loaded = False
            for item in news_items:
                headline_tag = await item.query_selector('a.title')
                if headline_tag:
                    headline = await headline_tag.inner_text()
                    url = await headline_tag.get_attribute('href')
                    if headline and url and not any(news["headline"] == headline for news in news_results):
                        news_results.append({"headline": headline, "url": url})
                        new_articles_loaded = True

            # If no new articles were loaded, break the loop
            if not new_articles_loaded:
                print(f"No new articles loaded after scroll {scroll + 1}. Ending scraping.")
                break

            print(f"Scroll {scroll + 1} loaded {len(news_items)} articles.")
            await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            await page.wait_for_timeout(scroll_pause)  # Wait for new content to load

        # Close the browser
        await browser.close()

    print("\nAll News Results:")
    for news in news_results:
        print(f"Headline: {news['headline']}")
        print(f"URL: {news['url']}\n")

# Run the async function
query = '"google"+"cloud"'
asyncio.run(fetch_bing_news(query=query, max_scrolls=20, scroll_pause=2000))
