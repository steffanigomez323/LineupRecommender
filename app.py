from flask import Flask, render_template, url_for

app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def home():
    return render_template('index.html')

@app.route('/writeup')
def writeup():
    return render_template('writeup.html')

if __name__ == "__main__":
    app.run(debug=True)