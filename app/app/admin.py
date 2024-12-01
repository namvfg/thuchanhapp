from tkinter import image_names

from flask import request
from flask_sqlalchemy.model import Model

from app.dao import count_product_by_receipt
from app.models import Product, Category, Tag
from app import db, appdemo, dao
from flask_admin import Admin, BaseView, expose, AdminIndexView
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user
from wtforms import TextAreaField
from wtforms.widgets import TextArea


class CKTextAreaWidget(TextArea):
    def __call__(self, field, **kwargs):
        if kwargs.get('class'):
            kwargs['class'] += ' ckeditor'
        else:
            kwargs.setdefault('class', 'ckeditor')
        return super(CKTextAreaWidget, self).__call__(field, **kwargs)

class CKTextAreaField(TextAreaField):
    widget = CKTextAreaWidget()

class MessageAdmin(ModelView):
    extra_js = ['//cdn.ckeditor.com/4.6.0/standard/ckeditor.js']

    form_overrides = {
        'body': CKTextAreaField
    }


class ProductView(ModelView):
    column_list = ['name', 'description', 'price', 'active'] #các cột có thể hiện
    column_labels = {  # tiêu đề của từng cột
        'name': 'Tên sản phẩm',
        'description': 'Mô tả',
        'price': 'Giá',
        'active': 'Còn bán'
    }
    extra_js = ['//cdn.ckeditor.com/4.6.0/standard/ckeditor.js']
    form_overrides = {
        "description": CKTextAreaField
    }

    column_searchable_list = ['name', 'description'] #có thể tìm theo các thuộc tính
    column_filters = ['name', 'price'] #có thể lọc theo các thuoc tính

    can_view_details = True #có thể xem chi tiết
    can_export = True #có thể xuất ra file excel

    def is_accessible(self):
        return current_user.is_authenticated


class CategoryView(ModelView):
    column_list = ['name', 'products']

    def is_accessible(self):
        return current_user.is_authenticated


class TagView(ModelView):

    def is_accessible(self):
        return current_user.is_authenticated


class StatsView(BaseView):
    @expose('/') #chỉ định đường dẫn để map vào admin
    def index(self):
        revenues = count_product_by_receipt(keyword=request.args.get("keyword"),
                                            from_date=request.args.get("from_date"),
                                            to_date=request.args.get("to_date"))
        return self.render('admin/stats.html', revenues=revenues)


class MyAdminView(AdminIndexView):
    @expose("/")
    def index(self):
        stats = dao.count_product_by_cate()
        return self.render("admin/index.html", stats=stats)


admin = Admin(app=appdemo, name="Quản trị bán hàng", template_mode="bootstrap4", index_view=MyAdminView())
admin.add_view(CategoryView(Category, db.session, name='Danh Mục'))
admin.add_view(ProductView(Product, db.session, name='Sản Phẩm'))
admin.add_view(TagView(Tag, db.session, name='Tag'))

admin.add_view(StatsView(name="Thống kê"))
