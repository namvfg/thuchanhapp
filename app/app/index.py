from flask import render_template
from app import dao
from app import appdemo


@appdemo.route("/")
def index():
    cates = dao.load_categories()
    prods = dao.load_products()
    return render_template("index.html",
                           categories=cates,
                           products=prods)

if __name__ == "__main__":
    appdemo.run(debug=True)