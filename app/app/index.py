from tempfile import template

from flask import Flask, render_template

appdemo = Flask(__name__)

@appdemo.route("/")
def index():
    return render_template("index.html")

if __name__ == "__main__":
    appdemo.run(debug=True)