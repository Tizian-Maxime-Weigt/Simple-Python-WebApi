import json
from flask import Flask, request, jsonify
from duckduckgo_search import DDGS

app = Flask(__name__)

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
    
    try:
        max_res = int(request.args.get('max_res', default_max_res))
    except (TypeError, ValueError):
        max_res = default_max_res

    results = DDGS().text(keywords, region='de-DE', max_results=max_res)
    
    formatted_ddg_results = format_ddg_results(results)

    results = {
        'TMW-Web-Api-v1.2': formatted_ddg_results,
    }

    return jsonify(results)

if __name__ == '__main__':
    app.run(host='0.0.0.0')
