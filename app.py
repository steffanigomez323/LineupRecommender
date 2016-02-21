from flask import Flask, render_template, redirect, url_for, request

app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def home():
    error = None

    return "Hello World!"

@app.route('/writeup')
def writeup():
    return render_template("writeup.html")

if __name__ == "__main__":
    app.run(debug=True)