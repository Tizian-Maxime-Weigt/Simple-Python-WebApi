import time
from collections import defaultdict
from urllib.parse import quote

from flask import Flask, request, jsonify
from duckduckgo_search import DDGS
from httpx import Client, Timeout
from parsel import Selector

app = Flask(__name__)

# Cache config
cache = {}
CACHE_TTL = 600

# HTTP client for Google scraping
client = Client(
    headers={
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/114.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9,de;q=0.8",
    },
    follow_redirects=True,
    http2=True,
    timeout=Timeout(10.0)
)

def parse_google_search_results(selector: Selector):
    results = []
    for box in selector.xpath("//div[@class='tF2Cxc']"):
        title = box.xpath(".//h3/text()").get()
        url = box.xpath(".//a/@href").get()
        snippet = box.xpath(".//div[@class='IsZvec']//span/text()").get()
        if not title or not url:
            continue
        results.append({
            "title": title,
            "link": url,
            "description": snippet or "",
        })
    return results

def scrape_google_search(query: str, max_results=6):
    url = f"https://www.google.com/search?hl=en&q={quote(query)}&num={max_results}"
    response = client.get(url)

    if response.status_code != 200:
        raise RuntimeError(f"Google search failed with status code {response.status_code}")

    if any(keyword in response.text.lower() for keyword in ["unusual traffic", "captcha", "sorry"]):
        raise RuntimeError("Blocked by Google CAPTCHA or rate limit.")

    selector = Selector(response.text)
    results = parse_google_search_results(selector)
    return results[:max_results]

def format_ddg_results(ddg_results):
    return [{
        'title': item['title'],
        'description': item['body'],
        'link': item['href'],
    } for item in ddg_results]

@app.route('/suche', methods=['GET'])
def suche():
    default_max_res = 6
    keywords = request.args.get('q')

    if not keywords:
        return jsonify({'error': 'Query parameter "q" is required'}), 400

    try:
        max_res = int(request.args.get('max_res', default_max_res))
    except (TypeError, ValueError):
        max_res = default_max_res

    search_engine = request.headers.get('X-Search-Engine', 'google').lower()
    cache_key = (keywords, max_res, search_engine)
    current_time = time.time()

    if cache_key in cache:
        cached_time, cached_results = cache[cache_key]
        if current_time - cached_time < CACHE_TTL:
            return jsonify(cached_results)

    try:
        if search_engine == 'duckduckgo':
            ddg_results = DDGS().text(keywords, region='de-DE', max_results=max_res)
            results = format_ddg_results(ddg_results)
        else:
            results = scrape_google_search(keywords, max_results=max_res)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

    response = {
        'search_engine': search_engine,
        'query': keywords,
        'results': results,
    }

    cache[cache_key] = (current_time, response)
    return jsonify(response)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
