from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return "Hello"

@app.route('/cameras')
def cameras():

