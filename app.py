from flask import Flask, jsonify
import json
from detector import Detector as Dt
#import limiter as lim
dt = Dt()

app = Flask(__name__)

@app.route('/')
def home():
    return "Hello"

@app.route('/cameras')
def cameras():
    #return  jsonify(dt.data_getter())
    return  jsonify({"cameras": [{"id": 2, "status": "1", "img": "fjd"}, {"id": 1, "status": "2", "img": "fjd"}, {"id": 1, "status": "2", "img": "fjd"}, {"id": 1, "status": "2", "img": "fjd"}]})

@app.route('/logs')
def logs():
    return logs
#
#@app.route('/inhibitor')
#def inhibitor ():
#    lim.poor_mode(20,200)
#    return lim.poor_mode
#
#@app.route('/activator')
#def activator():
#    lim.rich_mode()
#    return lim.rich_mode

    


