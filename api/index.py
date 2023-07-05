from flask import Flask, request, jsonify
from duckduckgo_search import ddg
from googleapiclient.discovery import build

app = Flask(__name__)

API_KEY = 'AIzaSyAd2QzPiLueo1n7UF910rQpXc3e-QmT-ZI'
CX = '300f61ad1f18d4ea8'

def google_search(query, num_results):
    service = build('customsearch', 'v1', developerKey=API_KEY)
    res = service.cse().list(q=query, cx=CX, num=num_results).execute()
    return [item['link'] for item in res.get('items', [])]

@app.route('/suche')
def suche():
    
    keywords = request.args.get('q')

    max_results = int("5")

    google_results = google_search(keywords, num_results=max_results)

    duckduckgo_results = ddg(keywords, region='de-DE', max_results=max_results)

    results = {
        'Google': google_results,
        'DuckDuckGo': duckduckgo_results
    }

    return jsonify(results)

if __name__ == '__main__':
    app.run(host='0.0.0.0')
