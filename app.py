from flask import Flask, render_template_string
from api.index import suche

app = Flask(__name__)

@app.route('/')
def home_wrapper():
    return render_tempalte('home.html')

@app.route('/suche')
def suche_wrapper():
    return suche()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
