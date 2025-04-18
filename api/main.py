from flask import Flask, jsonify, make_response, request
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import pytz

app = Flask(__name__)
def convert_date_to_days(stringdate):
    months = {'January':0,'February':31,'March':28,'April':31,'May':30} # days in month before
    end = 0
    for i in months:
        end += months[i]
        if stringdate.split(' ')[0] == i:
            break
    return end + int(stringdate.split(' ')[1])

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

@app.route('/soph-honors-today')
def soph_honors_today():
    today = datetime.now(pytz.timezone("America/Los_Angeles")).strftime('%B %d')
    dayname = datetime.now(pytz.timezone("America/Los_Angeles")).strftime('%A')
    r = requests.get('https://sklarnation.com/sophomore-honors-english').text
    soup = BeautifulSoup(r, 'html.parser')
    maindiv = soup.find_all('div', class_='entry-content')[0]
    foundweek = False
    for i in maindiv.find_all('p'):
        if i.text.startswith('Week'):
            if foundweek: break
            datestring = i.text.split('— ')[1].split(',')[0]
            dates = datestring.split('-')
            if not any(c.isalpha() for c in dates[1]): # checks if any alpha characters are present
                print("dates[1] isn't numeric")
                dates[1] = dates[0].split(' ')[0] + ' ' + dates[1]
            if convert_date_to_days(dates[0]) <= convert_date_to_days(today) <= convert_date_to_days(dates[1]):
                foundweek = True
        elif foundweek:
            if i.text.startswith(dayname):
                return i.text.split('— ')[1]
    return ''

def _build_cors_preflight_response():
    response = make_response()
    response.headers.add("Access-Control-Allow-Origin", "https://shibby360.github.io")
    response.headers.add('Access-Control-Allow-Headers', "*")
    response.headers.add('Access-Control-Allow-Methods', "*")
    return response

def _corsify_actual_response(response):
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response

if __name__ == '__main__':
    app.run()