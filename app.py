from flask import Flask, request
from api.index import suche

app = Flask(__name__)

app.route('/suche')(suche)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
