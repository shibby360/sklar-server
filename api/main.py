from flask import Flask
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route('/')
def home():
    return 'home'

@app.route('/soph-honors')
def soph_honors():
    r = requests.get('https://sklarnation.com/sophomore-honors-english').text
    soup = BeautifulSoup(r, 'html.parser')
    maindiv = soup.find_all('div', class_='entry-content')[0]
    return str(maindiv)
