from flask import Flask
from detector import Detector as Dt
dt = Dt()

app = Flask(__name__)

@app.route('/')
def home():
    return "Hello"

@app.route('/cameras')
def cameras():
    return  dt.data_getter()

@app.route('/status')
def status():
    return 

@app.route('/logs')
def logs():
    return


