from flask import render_template, request
from app import dao
from app import appdemo
from app.dao import get_product_by_id


@appdemo.route("/")
def index():
    cate_id = request.args.get("category_id")
    keyword = request.args.get("keyword")

    cates = dao.load_categories()
    prods = dao.load_products(cate_id=cate_id, keyword=keyword)
    return render_template("index.html",
                           categories=cates,
                           products=prods)

@appdemo.route("/product/<int:product_id>")
def details(product_id):
    product = get_product_by_id(product_id=product_id)
    return render_template("detail.html", product=product)

if __name__ == "__main__":
    appdemo.run(debug=True)