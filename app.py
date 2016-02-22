from flask import Flask, render_template, url_for
from redis import Redis

app = Flask(__name__)
app.database = Redis(host='aws-us-east-1-portal.6.dblayer.com', port=11509, password="RYABQWHKVGXBKGUR")

@app.route("/", methods=['GET', 'POST'])
def home():
    return render_template('index.html')

@app.route('/writeup')
def writeup():
    return render_template('writeup.html')

if __name__ == "__main__":
    app.run(debug=True)