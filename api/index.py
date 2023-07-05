from flask import Flask, request
from duckduckgo_search import ddg
app = Flask(__name__)
    
@app.route('/suche')
def suche():
    keywords = request.args.get('q')
    
    max_results = int(request.args.get('max_results') or "5")
    
    results = ddg(keywords, region='wt-wt', max_results=max_results)
    
    return results


if __name__ == '__main__':
    app.run(host='0.0.0.0')
