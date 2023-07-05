# python server
from selenium import webdriver
from flask import Flask, send_file
from arb import *
#bet in william hill
def bet_william_hill(url,team, odd, value):
    
    return "willian hill Success"

def bet_matchbook(url,team, odd, value):
    
    return "matchbook Success"



app = Flask(__name__)
app.debug = True

@app.route('/')
def index():
    return send_file('index.html')

@app.route('/style.css')
def css():
    return send_file('style.css')

@app.route('/script.js')
def js():
    return send_file('script.js')


@app.route('/beep.mp3')
def beep():
    return send_file('beep.mp3')

@app.route('/bets/data.json')
def getdata():
    return send_file('../bets/data.json')

@app.route('/findarbs')
def findArbs():
    result = FindArbs()
    return result

if __name__ == '__main__':
    app.run()