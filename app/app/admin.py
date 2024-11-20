from flask_sqlalchemy.model import Model

from app.models import Product, Category
from app import db, appdemo
from flask_admin import Admin, BaseView, expose
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user

class ProductView(ModelView):
    column_list = ['name', 'description', 'price', 'active', 'category'] #các cột có thể hiện

    column_searchable_list = ['name', 'description'] #có thể tìm theo các thuộc tính
    column_filters = ['name', 'price'] #có thể lọc theo các thuoc tính
    column_labels = {    #tiêu đề của từng cột
        'name': 'Tên sản phẩm',
        'description': 'Mô tả',
        'price': 'Giá',
        'category': 'Danh mục',
        'active': 'Còn bán'
    }

    form_columns = ['name', 'description', 'price', 'image', 'active', 'category_id'] #các cột hiện ra khi create

    can_view_details = True #có thể xem chi tiết
    can_export = True #có thể xuất ra file excel

    def is_accessible(self):
        return current_user.is_authenticated

class CategoryView(ModelView):
    pass


class StatsView(BaseView):
    @expose('/') #chỉ định đường dẫn để map vào admin
    def index(self):
        return self.render('admin/stats.html')



admin = Admin(app=appdemo, name="Quản trị bán hàng", template_mode="bootstrap4")
admin.add_view(CategoryView(Category, db.session, name='Danh Mục'))
admin.add_view(ProductView(Product, db.session, name='Sản Phẩm'))

admin.add_view(StatsView(name="Thống kê"))
