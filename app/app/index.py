import hashlib
import math
from itertools import product

from flask import render_template, request, redirect, session, jsonify
from app import dao
from app import appdemo, db, login, admin, utils, controller
from flask_login import login_user, logout_user, current_user, login_required
import cloudinary.uploader
from app.decorators import annonymous_user


############################### render ###############################

#trang chu index.html
appdemo.add_url_rule("/", "index", controller.index)

#chi tiet san pham
appdemo.add_url_rule("/product/<int:product_id>", "product_detail", controller.details)

#dang nhâp admin
appdemo.add_url_rule("/login-admin", "login_admin", controller.admin_login, methods=['post'])

#dang ky user
appdemo.add_url_rule("/register", "register", controller.register, methods=['post', 'get'])

#dang nhap user
appdemo.add_url_rule("/login", "login", controller.login_my_user, methods=["get", "post"])

#dang xuat user
appdemo.add_url_rule("/logout", "logout", controller.logout_my_user)

#gio hang
appdemo.add_url_rule("/cart", "cart", controller.cart)

###################################################################



############################### api ###############################

#api them hang vao gio hang
appdemo.add_url_rule("/api/cart", "api_cart", controller.add_to_cart, methods=["post"])

#api update gio hang
appdemo.add_url_rule("/api/cart/<product_id>", "api_cart_productId_update", controller.update_cart, methods=['put'])

#api xoa gio hang
appdemo.add_url_rule("/api/cart/<product_id>", "api_cart_productId_delete", controller.delete_cart, methods=['delete'])

#api thanh toan
appdemo.add_url_rule("/api/pay", "api_pay", controller.pay)

############################ end api ##################################



@appdemo.context_processor
def common_attr():
    cates = dao.load_categories()
    return {
        'categories': cates,
        'cart': utils.cart_stats(session.get(appdemo.config["CART_KEY"]))
    }

@login.user_loader
def load_user(userid):
    return dao.get_user_by_id(userid)




if __name__ == "__main__":
    appdemo.run(debug=True)