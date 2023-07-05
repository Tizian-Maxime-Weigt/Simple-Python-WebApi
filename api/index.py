from flask import Flask, request, jsonify
from ..googlesearch import search
from duckduckgo_search import ddg

app = Flask(__name__)

@app.route('/suche')
def suche():
    keywords = request.args.get('q')
    max_results = int(request.args.get('max_results') or "5")

    google_results = list(search(keywords, num=max_results))
    duckduckgo_results = ddg(keywords, region='de-DE', max_results=max_results)

    results = {
        'Google': google_results,
        'DuckDuckGo': duckduckgo_results
    }

    return jsonify(results)

if __name__ == '__main__':
    app.run(host='0.0.0.0')
