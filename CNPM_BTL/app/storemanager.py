# from flask_admin.contrib.sqla import ModelView
# from flask_admin import Admin, BaseView, expose, AdminIndexView
# from app import app, db, dao
# from flask_login import logout_user, current_user
# from app.models import Category, Product, UserRoleEnum, Author, User, ReceiptDetails, Quydinh, Receipt, Order
# from flask import redirect, request
#
#
# class AuthenticatedAdmin(ModelView):
#     def is_accessible(self):
#         return current_user.is_authenticated and current_user.user_role == UserRoleEnum.ADMIN
#
#
# class AuthenticatedUser(BaseView):
#     def is_accessible(self):
#         return current_user.is_authenticated
#
#
# # class AuthenticatedStaff(BaseView):
# #     def is_accessible(self):
# #         return current_user.is_authenticated and current_user.user_role == UserRoleEnum.STAFF
#
#
# class MyAdminIndexView(AdminIndexView):
#     @expose('/')
#     def index(self):
#         return self.render('admin/index.html', stats=dao.count_products_by_cate())
#
#
# admin = Admin(app=app, name='Trang chủ admin', template_mode='bootstrap4', index_view=MyAdminIndexView())
#
#
# class MyProductView(AuthenticatedAdmin):
#     column_list = ['id', 'name', 'price', 'category', 'author', 'quantity']
#     can_export = True
#     column_searchable_list = ['name']
#     column_filters = ['price', 'name']
#     column_editable_list = ['name', 'price']
#     details_modal = True
#     edit_modal = True
#     can_view_details = True
#
#
# class MyCategoryView(AuthenticatedAdmin):
#     column_list = ['name', 'product_id']
#
#
# class MyAuthorView(AuthenticatedAdmin):
#     column_list = ['name', 'product_id']
#
#
# class UserView(AuthenticatedAdmin):
#     import hashlib
#     column_list = ['name', 'username', 'user_role']
#     # password = str(hashlib.md5(User.password.strip().encode('utf-8')).hexdigest())
#     can_view_details = True
#
#
# class QuydinhView(AuthenticatedAdmin):
#     column_list = ['id', 'name']
#
#
# class ReceiptsView(AuthenticatedAdmin):
#     column_list = ['id', 'product_id', 'created_date', 'quantity']
#
#
# class OrdersView(AuthenticatedAdmin):
#     column_list = ['id', 'order_date']
#
#
# class StatsView(AuthenticatedUser):
#     @expose("/")
#     def index(self):
#         return self.render('admin/stats.html')
#
#
# class LogoutView(AuthenticatedUser):
#     @expose("/")
#     def index(self):
#         logout_user()
#
#         return redirect('/login')
#
#
# admin.add_view(MyCategoryView(Category, db.session, name="Thể loại"))
# admin.add_view(MyProductView(Product, db.session, name="Sách"))
# admin.add_view(MyAuthorView(Author, db.session, name="Tác giả"))
# admin.add_view(UserView(User, db.session, name="Tài khoản"))
# admin.add_view(ReceiptsView(ReceiptDetails, db.session, name="Hóa đơn"))
# admin.add_view(OrdersView(Order, db.session, name="Nhập hàng"))
# admin.add_view(QuydinhView(Quydinh, db.session, name="Quy định"))
# admin.add_view(StatsView(name='Thống kê báo cáo'))
# admin.add_view(LogoutView(name='Đăng xuất'))