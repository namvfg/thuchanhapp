from flask_sqlalchemy.model import Model

from app.models import Product, Category
from app import db, appdemo
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView


admin = Admin(app=appdemo, name="Quản trị bán hàng", template_mode="bootstrap4")
admin.add_view(ModelView(Category, db.session))
admin.add_view(ModelView(Product, db.session))
