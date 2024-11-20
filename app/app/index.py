import math

from flask import render_template, request, redirect
from app import dao
from app import appdemo, db, login
from flask_login import login_user
from app import admin
from app.dao import get_product_by_id, get_user_by_id


@appdemo.route("/")
def index():
    cate_id = request.args.get("category_id")
    keyword = request.args.get("keyword")
    page = request.args.get("page", 1)

    page_size = appdemo.config["PAGE_SIZE"]

    page_count = dao.count_product()

    prods = dao.load_products(cate_id=cate_id, keyword=keyword, page=int(page))
    return render_template("index.html",
                           products=prods,
                           pages=math.ceil(page_count/page_size))


@appdemo.route("/product/<int:product_id>")
def details(product_id):
    product = get_product_by_id(product_id=product_id)
    return render_template("detail.html", product=product)

@appdemo.route("/login-admin", methods=['post'])
def admin_login():
    username = request.form['username']
    password = request.form['password']

    user = dao.auth_user(username=username, password=password)
    if user:
        login_user(user=user)

    return redirect('/admin')

@appdemo.context_processor
def common_attr():
    cates = dao.load_categories()
    return {
        'categories': cates
    }

@login.user_loader
def load_user(userid):
    return get_user_by_id(userid)




if __name__ == "__main__":
    appdemo.run(debug=True)