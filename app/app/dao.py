import json
from app import appdemo


def load_categories():
    with open("%s/data/categories.json" % appdemo.root_path, encoding='utf-8') as f:
        return json.load(f)

def load_products(cate_id=None):
    with open("%s/data/products.json" % appdemo.root_path, encoding='utf-8') as f:
        products = json.load(f)

    if cate_id:
        products = [prod for prod in products if prod["category_id"] == int(cate_id)]

    return products