from flask import render_template
from app import dao
from app import appdemo


@appdemo.route("/")
def index():
    cates = dao.load_categories()
    return render_template("index.html", categories = cates)

if __name__ == "__main__":
    appdemo.run(debug=True)