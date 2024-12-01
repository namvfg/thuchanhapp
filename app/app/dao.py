from itertools import product

from flask_login import current_user
from sqlalchemy import func
from app import appdemo, db
from app.models import Category, Product, User, Receipt, ReceiptDetails
from flask import request
import hashlib


def load_categories():
    return Category.query.order_by("id").all()

def load_products(cate_id=None, keyword=None, page=1):
    products = Product.query

    if cate_id:
        products = products.filter(Product.category_id.__eq__(cate_id))

    if keyword:
        products = products.filter(Product.name.contains(keyword))

    page_size = appdemo.config["PAGE_SIZE"]
    start = (page - 1) * page_size
    products = products.slice(start, start + page_size)

    return products.all()

def count_product():
    return Product.query.count()

def get_product_by_id(product_id):
    return Product.query.get(product_id)

def auth_user(username, password):
    password = str(hashlib.md5(password.strip().encode("utf-8")).digest())

    return User.query.filter(User.username.__eq__(username.strip()), User.password.__eq__(password)).first()

def get_user_by_id(userid):
    return User.query.get(userid)


def register(name, username, password, avatar):
    password = str(hashlib.md5(password.strip().encode("utf-8")).digest())
    u = User(name=name, username=username,
             password = password,
             avatar = avatar)
    db.session.add(u)
    db.session.commit()


def save_receipt(cart):
    if cart:
        receipt = Receipt(user=current_user) #user được khai báo ở backref
        db.session.add(receipt)

        for c in cart.values():
            detail = ReceiptDetails(quantity=c["quantity"], price=c["price"],
                                    receipt=receipt, product_id=c["id"]) #receipt truyen doi tuong vi chua luu receipt
            db.session.add(detail)
        db.session.commit()


def count_product_by_cate():
    return db.session.query(Category.id, Category.name, func.count(Product.id))\
            .join(Product, Product.category_id.__eq__(Category.id), isouter=True)\
            .group_by(Category.id).all()

def count_product_by_receipt(keyword=None, from_date=None, to_date=None):
    query = db.session.query(Product.id, Product.name, func.sum(ReceiptDetails.product_id)\
        , func.sum(ReceiptDetails.quantity * ReceiptDetails.price))\
        .join(ReceiptDetails, Product.id.__eq__(ReceiptDetails.product_id))\
        .join(Receipt, Receipt.id.__eq__(ReceiptDetails.receipt_id))\
        .group_by(Product.id)

    if keyword:
        query = query.filter(Product.name.contains(keyword))

    if from_date:
        query = query.filter(Receipt.created_date.__ge__(from_date))

    if to_date:
        query = query.filter(Receipt.created_date.__le__(to_date))

    return query


if __name__ == "__main__":
    from app import appdemo
    with appdemo.app_context():
        print(count_product_by_receipt())