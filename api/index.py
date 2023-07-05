from flask import Flask, request, jsonify
from duckduckgo_search import ddg
from search_google.api import GoogleSearch

app = Flask(__name__)

API_KEY = 'your_api_key'
CX = 'your_cse_id'

def google_search(query, num_results):
    search = GoogleSearch(buildargs={'developerKey': API_KEY}, cseargs={'cx': CX, 'q': query, 'num': num_results})
    results = search.get_dict()
    return [item['link'] for item in results['items']]

@app.route('/suche')
def suche():
    keywords = request.args.get('q')
    max_results = 5

    google_results = google_search(keywords, num_results=max_results)
    duckduckgo_results = ddg(keywords, region='de-DE', max_results=max_results)

    results = {
        'Google': google_results,
        'DuckDuckGo': duckduckgo_results
    }

    return jsonify(results)

if __name__ == '__main__':
    app.run(host='0.0.0.0')
