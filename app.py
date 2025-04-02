from flask import Flask, request, render_template_string
from api.index import suche
app = Flask(__name__)

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

@app.route('/')
def home():
    return index()
    
@app.route('/home')
def home():
    return index()

@app.route('/suche')
def suche_wrapper():
    return suche()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=False)
