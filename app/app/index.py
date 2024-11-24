import hashlib
import math

from flask import render_template, request, redirect, session
from app import dao
from app import appdemo, db, login, admin
from flask_login import login_user, logout_user, current_user
import cloudinary.uploader
from app.decorators import annonymous_user


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
    product = dao.get_product_by_id(product_id=product_id)
    return render_template("detail.html", product=product)

@appdemo.route("/login-admin", methods=['post'])
def admin_login():
    username = request.form['username']
    password = request.form['password']

    user = dao.auth_user(username=username, password=password)
    if user:
        login_user(user=user)

    return redirect('/admin')

@appdemo.route("/register", methods=['post', 'get'])
def register():
    err_msg = ""
    if request.method.__eq__('POST'):
        password = request.form["password"]
        confirm_password = request.form["confirm-password"]
        if password.__eq__(confirm_password):
            #upload
            avatar = ""
            res = cloudinary.uploader.upload(request.files["avatar"])
            avatar = res["secure_url"]
            #save user
            try:
                dao.register(name=request.form["name"],
                             username=request.form["username"],
                             password=password,
                             avatar=avatar)
                return redirect("/login")
            except:
                err_msg = "Hệ thống đang có lỗi! Vui lòng thử lại sau"
        else:
            err_msg = "Mật khẩu không khớp"

    return render_template("register.html", err_msg=err_msg)

@appdemo.route("/login", methods=["get", "post"])
@annonymous_user
def login_my_user():
    if request.method.__eq__("POST"):
        username = request.form["username"]
        password = request.form["password"]
        user = dao.auth_user(username.strip(), password)
        if user:
            login_user(user=user)
            return redirect("/")
    return render_template("login.html")

@appdemo.route("/logout")
def logout_my_user():
    logout_user()
    return redirect("/login")

@appdemo.route("/cart")
def cart():
    session["cart"] = {
        "1": {
            "id": "1",
            "name": "iphone 13",
            "price": 12000000,
            "quantity": 10,
        },
        "2": {
            "id": "2",
            "name": "iphone 14",
            "price": 24000000,
            "quantity": 15,
        }
    }
    return render_template("cart.html")

@appdemo.context_processor
def common_attr():
    cates = dao.load_categories()
    return {
        'categories': cates
    }

@login.user_loader
def load_user(userid):
    return dao.get_user_by_id(userid)




if __name__ == "__main__":
    appdemo.run(debug=True)