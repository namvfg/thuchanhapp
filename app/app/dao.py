
from app import appdemo
from app.models import Category, Product


def load_categories():
    return Category.query.order_by("id").all()

def load_products(cate_id=None, keyword=None):
    products = Product.query

    if cate_id:
        products = products.filter(Product.category_id.__eq__(cate_id))

    if keyword:
        products = products.filter(Product.name.contains(keyword))

    return products.all()

def get_product_by_id(product_id):
    return Product.query.get(product_id)
