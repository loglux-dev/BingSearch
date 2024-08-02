import asyncio
from playwright.async_api import async_playwright

async def fetch_bing_news(query, max_scrolls=10, scroll_pause=3000):
    async with async_playwright() as p:
        # Launch the browser
        browser = await p.chromium.launch(headless=True)  # Use headless=True in production
        page = await browser.new_page()

        # Navigate to Bing News search with the specified query
        await page.goto(f"https://www.bing.com/news/search?q={query}")

        # Store the results in a list
        news_results = []

        # Perform scrolling to load more results
        for scroll in range(max_scrolls):
            # Extract news headlines, URLs, publication dates, and snippets
            news_items = await page.query_selector_all('div.news-card')

            new_articles_loaded = False
            for item in news_items:
                headline_tag = await item.query_selector('a.title')
                date_tag = await item.query_selector('span[aria-label]')
                snippet_tag = await item.query_selector('div.snippet')

                if headline_tag:
                    headline = await headline_tag.inner_text()
                    url = await headline_tag.get_attribute('href')
                    pub_date = await date_tag.get_attribute('aria-label') if date_tag else 'No date available'
                    snippet = await snippet_tag.inner_text() if snippet_tag else 'No snippet available'

                    if headline and url and not any(news["headline"] == headline for news in news_results):
                        news_results.append({
                            "headline": headline,
                            "url": url,
                            "date": pub_date,
                            "snippet": snippet
                        })
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
        print(f"URL: {news['url']}")
        print(f"Date: {news['date']}")
        print(f"Snippet: {news['snippet']}\n")

# Run the async function
query = '"google"+"cloud"'
asyncio.run(fetch_bing_news(query=query, max_scrolls=20, scroll_pause=2000))
