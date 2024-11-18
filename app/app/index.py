import math

from flask import render_template, request
from app import dao
from app import appdemo
from app import admin
from app.dao import get_product_by_id


@appdemo.route("/")
def index():
    cate_id = request.args.get("category_id")
    keyword = request.args.get("keyword")
    page = request.args.get("page", 1)

    page_size = appdemo.config["PAGE_SIZE"]

    page_count = dao.count_product()
    cates = dao.load_categories()
    prods = dao.load_products(cate_id=cate_id, keyword=keyword, page=int(page))
    return render_template("index.html",
                           categories=cates,
                           products=prods,
                           pages=math.ceil(page_count/page_size))


@appdemo.route("/product/<int:product_id>")
def details(product_id):
    product = get_product_by_id(product_id=product_id)
    return render_template("detail.html", product=product)

if __name__ == "__main__":
    appdemo.run(debug=True)