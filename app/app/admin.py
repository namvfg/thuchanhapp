from flask_sqlalchemy.model import Model

from app.models import Product, Category
from app import db, appdemo
from flask_admin import Admin, BaseView, expose
from flask_admin.contrib.sqla import ModelView

class ProductView(ModelView):
    column_list = ['name', 'description', 'price', 'active', 'category']

    column_searchable_list = ['name', 'description']
    column_filters = ['name', 'price']
    column_labels = {
        'name': 'Tên sản phẩm',
        'description': 'Mô tả',
        'price': 'Giá',
        'category': 'Danh mục',
        'active': 'Còn bán'
    }

    form_columns = ['name', 'description', 'price', 'image', 'active', 'category_id']

    can_view_details = True
    can_export = True

class CategoryView(ModelView):
    column_list = ['name', 'products']


class StatsView(BaseView):
    @expose('/') #chỉ định đường dẫn để map vào admin
    def index(self):
        return self.render('admin/stats.html')



admin = Admin(app=appdemo, name="Quản trị bán hàng", template_mode="bootstrap4")
admin.add_view(CategoryView(Category, db.session, name='Danh Mục'))
admin.add_view(ProductView(Product, db.session, name='Sản Phẩm'))

admin.add_view(StatsView(name="Thống kê"))
