from flask import Flask, render_template, url_for
from redis import Redis
from swish import SwishScraper

## CONFIG
REDIS_HOST = 'aws-us-east-1-portal.6.dblayer.com'
REDIS_PASSWORD = 'RYABQWHKVGXBKGUR'
REDIS_PORT = 11509
SWISH_URL = 'https://www.swishanalytics.com/optimus/nba/optimus-x'

app = Flask(__name__)
app.database = Redis(host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASSWORD)

@app.route("/", methods=['GET', 'POST'])
def home():
    ss = SwishScraper(SWISH_URL)
    json_data = ss.get_request()
    clean_data = ss.clean_data(json_data)
    return render_template('index.html', players=clean_data)

@app.route('/writeup')
def writeup():
    return render_template('writeup.html')

if __name__ == "__main__":
    app.run(debug=True)