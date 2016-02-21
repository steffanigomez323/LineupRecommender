from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World!"

@app.route('/writeup')
def writeup():
    return render_template("writeup.html")

if __name__ == "__main__":
    app.run(debug=True)