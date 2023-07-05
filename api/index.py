from flask import Flask, request, jsonify
from googleapiclient.discovery import build
from duckduckgo_search import ddg

app = Flask(__name__)

API_KEY = 'AIzaSyAd2QzPiLueo1n7UF910rQpXc3e-QmT-ZI'
CX = '300f61ad1f18d4ea8'

def google_search(query, num_results):
    service = build("customsearch", "v1", developerKey=API_KEY)
    res = service.cse().list(q=query, cx=CX, num=num_results).execute()
    results = []
    for item in res['items']:
        result = {
            'title': item['title'],
            'description': item['snippet'],
            'link': item['link']
        }
        results.append(result)
    return results

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
    keywords = request.args.get('q')
    max_results = int(request.args.get('max_results', 5))

    google_results = google_search(keywords, num_results=max_results)
    ddg_results = ddg(keywords, region='de-DE', max_results=max_results)
    formatted_ddg_results = format_ddg_results(ddg_results)

    results = {
        'Google': google_results,
        'DuckDuckGo': formatted_ddg_results
    }

    return jsonify(results)

if __name__ == '__main__':
    app.run(host='0.0.0.0')