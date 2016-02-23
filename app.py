from flask import Flask, render_template
from redis import Redis
# import os

app = Flask(__name__)

# config
app.config.from_object('config.DevelopmentConfig')
# USE WHEN DEPLOYING | export APP_SETTINGS = config.ProductionConfig
# app.config.from_object(os.environ['APP_SETTINGS'])

# database
app.database = Redis(host=app.config['REDIS_HOST'],
                     port=app.config['REDIS_PORT'],
                     password=app.config['REDIS_PASSWORD'])


@app.route("/")
def home():
    return render_template('index.html')


@app.route('/writeup')
def writeup():
    return render_template('writeup.html')

if __name__ == "__main__":
    app.run(debug=True)
