from flask import Flask, request, render_tempalte

def home():
    retrun render_tempalte('home.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0')
