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

@app.route('/')
def index():
    html_content = '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Basic WebAPI</title>
    </head>
    <body>
        <h1>Welcome to the Basic WebAPI</h1>
        <h1>Usage:</h1>
        <h1>/suche?q=<query>&max_res=<maximum_results></h1>
    </body>
    </html>
    '''
    return render_template_string(html_content)

@app.route('/suche')
def suche():
    max_results = 4
    
    keywords = request.args.get('q')
    max_res = int(request.args.get('max_res'))

    results = DDGS().text(keywords, region='de-DE', max_results=max_res)
    
    formatted_ddg_results = format_ddg_results(results)

    results = {
        'Web-API-v1.1': formatted_ddg_results,
    }

    return jsonify(results)

if __name__ == '__main__':
    app.run(host='0.0.0.0')
