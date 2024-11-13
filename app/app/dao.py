import json
from app import appdemo


def load_categories():
    with open("%s/data/categories.json" % appdemo.root_path, encoding='utf-8') as f:
        return json.load(f)

def load_products():
    with open("%s/data/products.json" % appdemo.root_path, encoding='utf-8') as f:
        return json.load(f)