import json
from flask import Flask, request, jsonify
from duckduckgo_search import DDGS
import time

app = Flask(__name__)

# Adding an Cache for queries
cache = {}
CACHE_TTL = 600

def format_ddg_results(ddg_results):
    results = []
    for item in ddg_results:
        result = {
            'title': item['title'],
            'description': item['body'],
            'link': item['href']
        }
        results.append(result)
    return results

@app.route('/suche')
def suche():
    default_max_res = 6
    
    keywords = request.args.get('q')
    if not keywords:
        return jsonify({'error': 'Query parameter q is required'}), 400
    
    try:
        max_res = int(request.args.get('max_res', default_max_res))
    except (TypeError, ValueError):
        max_res = default_max_res

    cache_key = (keywords, max_res)
    current_time = time.time()

    if cache_key in cache:
        cached_time, cached_results = cache[cache_key]
        if current_time - cached_time < CACHE_TTL:
            # Return cached results
            return jsonify(cached_results)
            
    results = DDGS().text(keywords, region='de-DE', max_results=max_res)
    formatted_ddg_results = format_ddg_results(results)

    response = {
        'TMW-Web-Api-v1.2': formatted_ddg_results,
    }

    # Store in cache
    cache[cache_key] = (current_time, response)

    return jsonify(response)

if __name__ == '__main__':
    app.run(host='0.0.0.0')
