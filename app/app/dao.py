from app import appdemo
from app.models import Category, Product


def load_categories():
    return Category.query.all()

def load_products(cate_id=None):
    products = Product.query

    if cate_id:
        products = products.filter(Product.category_id.__eq__(cate_id))

    return products.all()