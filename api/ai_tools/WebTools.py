from camoufox.sync_api import Camoufox
from browserforge.fingerprints import FingerprintGenerator
import urllib.parse

def url_encode(text: str) -> str:
    return urllib.parse.quote(text, safe='')

cache_questions: dict = {}

def search_the_web(question: str):
    """
    Search information in web
    
    question: str - request to search api
    """

    if question in cache_questions:
        return cache_questions.get(question)

    fg = FingerprintGenerator(browser='firefox')

    json = []

    with Camoufox(
            fingerprint=fg.generate(),
            humanize=True,
            i_know_what_im_doing=True,
            headless="virtual"
            ) as browser:
        page = browser.new_page()

        search_engine_url = "https://duckduckgo.com/?q=" + url_encode(question)

        page.goto(search_engine_url)

        results = page.locator('article[data-testid="result"]')

        count = results.count()

        for i in range(count):
            result = results.nth(i)

            link_el = result.locator('a[data-testid="result-title-a"]')

            title = link_el.inner_text()
            href = link_el.get_attribute('href')

            snippet_el = result.locator('[data-result="snippet"]')
            snippet = snippet_el.inner_text()

            json.append({
                "title": title,
                "desc": snippet,
                "link": href
            })
        
        cache_questions[question] = json

        return json
    
cache_urls: dict = {}

def go_to(url: str):
    """
    Get site content by url
    
    url: str - url to page for read
    """
    if url in cache_urls:
        return cache_urls.get(url)

    fg = FingerprintGenerator(browser='firefox')

    with Camoufox(
            fingerprint=fg.generate(),
            humanize=True,
            i_know_what_im_doing=True
            ) as browser:
        page = browser.new_page()

        page.goto(url)

        text = page.inner_text("body")

        cache_urls[url] = text

        return text
