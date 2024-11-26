
from app import appdemo, db
from app.models import Category, Product, User
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