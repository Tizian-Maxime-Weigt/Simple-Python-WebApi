import time
import asyncio
from concurrent.futures import ThreadPoolExecutor
from flask import Flask, request, jsonify
from duckduckgo_search import DDGS
import threading

app = Flask(__name__)

# Cache configuration with thread-safe dictionary
cache = {}
cache_lock = threading.RLock()
CACHE_TTL = 600

# Thread pool for async operations
executor = ThreadPoolExecutor(max_workers=4)

# Reuse DDGS instance to avoid initialization overhead
ddgs_instance = DDGS()

def format_ddg_results(ddg_results):
    """Optimized result formatting with list comprehension"""
    return [{
        'title': item['title'],
        'description': item['body'],
        'link': item['href'],
    } for item in ddg_results]

def get_from_cache(cache_key, current_time):
    """Thread-safe cache retrieval"""
    with cache_lock:
        if cache_key in cache:
            cached_time, cached_results = cache[cache_key]
            if current_time - cached_time < CACHE_TTL:
                return cached_results
    return None

def set_cache(cache_key, current_time, response):
    """Thread-safe cache setting"""
    with cache_lock:
        cache[cache_key] = (current_time, response)

def search_ddg(keywords, max_res):
    """Separate function for DuckDuckGo search to enable threading"""
    try:
        ddg_results = ddgs_instance.text(keywords, region='de-DE', max_results=max_res)
        return format_ddg_results(ddg_results)
    except Exception as e:
        raise e

@app.route('/suche')
def suche():
    default_max_res = 6
    keywords = request.args.get('q')
    if not keywords:
        return jsonify({'error': 'Query parameter q is required'}), 400

    # Optimize parameter parsing
    max_res_param = request.args.get('max_res')
    if max_res_param and max_res_param.isdigit():
        max_res = int(max_res_param)
    else:
        max_res = default_max_res

    cache_key = (keywords, max_res)
    current_time = time.time()

    # Check cache first
    cached_result = get_from_cache(cache_key, current_time)
    if cached_result:
        return jsonify(cached_result)

    # Perform search in thread pool for better concurrency
    try:
        future = executor.submit(search_ddg, keywords, max_res)
        results = future.result(timeout=10)  # 10 second timeout
    except Exception as e:
        return jsonify({'error': str(e)}), 500

    response = {
        'query': keywords,
        'results': results,
    }

    # Cache the result
    set_cache(cache_key, current_time, response)
    return jsonify(response)

def start_cache_cleanup():
    """Start periodic cache cleanup to prevent memory leaks"""
    def clean():
        current_time = time.time()
        with cache_lock:
            expired_keys = [k for k, (t, _) in cache.items() if current_time - t > CACHE_TTL]
            for key in expired_keys:
                del cache[key]
        # Schedule next cleanup
        threading.Timer(CACHE_TTL, clean).start()
    
    threading.Timer(CACHE_TTL, clean).start()

# Start cache cleanup when the module is imported
start_cache_cleanup()

if __name__ == '__main__':
    print("Starting server...")
    app.run(host='0.0.0.0', port=8080, threaded=True)
