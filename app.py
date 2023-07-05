from flask import Flask, request
from api.index import suche
app = Flask(__name__)


app.route('/suche')(suche)

@app.route('/')
def index():
    html_content = '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Tizi-Web Api</title>
    </head>
    <body>
        <h1>Welcome to the Tizi-Web Api!</h1>
        <h1>Doc comming Soon!</h1>
    </body>
    </html>
    '''
    return render_template_string(html_content)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
