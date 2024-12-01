import hashlib
import math
from itertools import product

from flask import render_template, request, redirect, session, jsonify
from app import dao
from app import appdemo, db, login, admin, utils
from flask_login import login_user, logout_user, current_user, login_required
import cloudinary.uploader
from app.decorators import annonymous_user


############################### render ###############################


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


def details(product_id):
    product = dao.get_product_by_id(product_id=product_id)
    return render_template("detail.html", product=product)


def admin_login():
    username = request.form['username']
    password = request.form['password']

    user = dao.auth_user(username=username, password=password)
    if user:
        login_user(user=user)

    return redirect('/admin')


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


@annonymous_user
def login_my_user():
    if request.method.__eq__("POST"):
        username = request.form["username"]
        password = request.form["password"]
        user = dao.auth_user(username.strip(), password)
        if user:
            login_user(user=user)
            next = request.args.get("next")
            return redirect(next if next else "/")
    return render_template("login.html")


def logout_my_user():
    logout_user()
    return redirect("/login")


def cart():
    # session[appdemo.config["CART_KEY"]] = {
    #     "1": {
    #         "id": "1",
    #         "name": "iphone 13",
    #         "price": 12000000,
    #         "quantity": 10,
    #     },
    #     "2": {
    #         "id": "2",
    #         "name": "iphone 14",
    #         "price": 24000000,
    #         "quantity": 15,
    #     }
    # }
    return render_template("cart.html")

###################################################################



############################### api ###############################

def add_to_cart():
    data = request.json
    id = str(data["id"]) #parse thành str để tiện làm key

    key = appdemo.config["CART_KEY"] #"cart"
    cart = session[key] if key in session else {}
    if id in cart:
        cart[id]["quantity"] += 1
    else:
        name = data["name"]
        price = data["price"]
        cart[id] = {
            "id": id,
            "name": name,
            "price": price,
            "quantity": 1,
        }
    session[key] = cart
    return jsonify(utils.cart_stats(cart=cart))


def update_cart(product_id):
    key = appdemo.config["CART_KEY"]  # "cart"
    cart = session.get(key)

    if cart and product_id in cart:
        cart[product_id]['quantity'] = int(request.json['quantity'])

    session[key] = cart
    return jsonify(utils.cart_stats(cart=cart))


def delete_cart(product_id):
    key = appdemo.config["CART_KEY"]  # "cart"
    cart = session.get(key)

    if cart and product_id in cart:
        del cart[product_id]

    session[key] = cart
    return jsonify(utils.cart_stats(cart=cart))


 #không cần methods vì không lấy hay gửi dữ liệu lên server, lấy dữ liệu từ session
@login_required
def pay():
    key = appdemo.config["CART_KEY"]  # "cart"
    cart = session.get(key)

    try:
        dao.save_receipt(cart)
    except:
        return jsonify({"status": 500})
    else:
        del(session[key])

    return jsonify({"status": 200})

############################ end api ##################################