from flask import Flask, jsonify, make_response, request
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route('/')
def home():
    return 'home'

@app.route('/soph-honors')
def soph_honors():
    if request.method == 'OPTIONS': # CORS preflight
        return _build_cors_preflight_response()
    elif request.method == 'GET': # The actual request following the preflight
        r = requests.get('https://sklarnation.com/sophomore-honors-english').text
        soup = BeautifulSoup(r, 'html.parser')
        maindiv = soup.find_all('div', class_='entry-content')[0]
        return _corsify_actual_response(make_response(str(maindiv)))


def _build_cors_preflight_response():
    response = make_response()
    response.headers.add("Access-Control-Allow-Origin", "https://shibby360.github.io") # change this later to only allow github pages site
    response.headers.add('Access-Control-Allow-Headers', "*")
    response.headers.add('Access-Control-Allow-Methods', "*")
    return response

def _corsify_actual_response(response):
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response
