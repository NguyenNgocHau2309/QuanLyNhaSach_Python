from datetime import datetime

from app import db, app
from sqlalchemy import Column, Integer, String, Float, ForeignKey, Enum, Boolean, DateTime
from sqlalchemy.orm import relationship
from flask_login import UserMixin
import hashlib, enum
from datetime import datetime


class UserRoleEnum(enum.Enum):
    USER = 1
    ADMIN = 2
    STAFF = 3
    WM = 4


# class Category(db.Model):
#     id = Column(Integer, primary_key=True, autoincrement=True)
#     name = Column(String(50), nullable=False, unique=True)
#     products = relationship('Product', backref='category', lazy=True)
#
#     def __str__(self):
#         return self.name
#
#
# class Product(db.Model):
#     id = Column(Integer, primary_key=True, autoincrement=True)
#     name = Column(String(50), nullable=False, unique=True)
#     price = Column(Float, default=0)
#     image = Column(String(200))
#     category_id = Column(Integer, ForeignKey(Category.id), nullable=False)
#     receipt_detail = relationship('ReceiptDetails', backref='product', lazy=True)
#
#     def __str__(self):
#         return self.name
#
#


class BaseModel(db.Model):
    __abstract__ = True
    created_date = Column(DateTime, default=datetime.now())
    active = Column(Boolean, default=True)
    id = Column(Integer, primary_key=True, autoincrement=True)


# class Receipt(BaseModel):
#     user_id = Column(Integer, ForeignKey(User.id),nullable=False)
#     receipt_detail = relationship('ReceiptDetails', backref='receipt', lazy=True)
#
#
# class ReceiptDetails(BaseModel):
#     quantity = Column(Integer, default=0)
#     price = Column(Float, default=0)
#     receipt_id = Column(Integer, ForeignKey(Receipt.id),nullable=False)
#     product_id = Column(Integer, ForeignKey(Product.id),nullable=False)
#
#     def __str__(self):
#         return self.name

# class Userrole(db.Model, UserMixin):
#     id = Column(Integer,primary_key=True,autoincrement=True)
#     user_role = Column(Enum(UserRoleEnum), default=UserRoleEnum.USER)
#     users = relationship('User', backref='userrole', lazy=True)


# class Customer(db.Model):
#     id = Column(Integer, primary_key=True, autoincrement=True)
#     email = Column(String(50))
#     phone = Column(String(50))
#     user_id = relationship('User', backref='customer', lazy=True)
#     receipts = relationship('Receipt', backref='customer', lazy=True)


class User(db.Model, UserMixin):
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False, unique=True)
    username = Column(String(50), nullable=False, unique=True)
    password = Column(String(100), nullable=False)
    avatar = Column(String(100),
                    default='https://res.cloudinary.com/dxxwcby8l/image/upload/v1688179242/hclq65mc6so7vdrbp7hz.jpg')
    receipts = relationship('Receipt', backref='user', lazy=True)  # các receipts user đã từng mua
    # userrole_id = Column(Integer,ForeignKey(Userrole.id), nullable=False, default=4)
    quydinh_detail = relationship('QuydinhDetail', backref='user', lazy=True)
    # customer_id = Column(Integer,ForeignKey(Customer.id), nullable=False)
    orders = relationship('Order', backref='user', lazy=True)
    user_role = Column(Enum(UserRoleEnum), default=UserRoleEnum.USER)
    comments = relationship('Comment', backref='user', lazy=True)


class Quydinh(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    quydinh_detail = relationship('QuydinhDetail', backref='quydinh', lazy=True)


class QuydinhDetail(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey(User.id), nullable=False)
    quydinh_id = Column(Integer, ForeignKey(Quydinh.id), nullable=False)
    changed_date = Column(DateTime, default=datetime.now())
    changed_content = Column(String(100))


class Category(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    product_id = relationship('Product', backref='category', lazy=True)

    def __str__(self):
        return self.name


class Author(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    product_id = relationship('Product', backref='author', lazy=True)

    def __str__(self):
        return self.name


class Product(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    quantity = Column(Integer, default=0)
    price = Column(Float, default=0)
    image = Column(String(200))
    active = Column(Boolean, default=True)
    author_id = Column(Integer, ForeignKey(Author.id), nullable=False)
    category_id = Column(Integer, ForeignKey(Category.id), nullable=False)
    order_detail = relationship('OrderDetails', backref='product', lazy=True)
    comments = relationship('Comment',backref='product', lazy=True)

    def __str__(self):
        return self.name


class Receipt(BaseModel):
    amount = Column(Float, default=0)
    user_id = Column(Integer, ForeignKey(User.id), nullable=False)
    receipt_detail = relationship('ReceiptDetails', backref='receipt', lazy=True)


class ReceiptDetails(BaseModel):
    quantity = Column(Integer, default=0)
    price = Column(Float, default=0)
    product_id = Column(Integer, ForeignKey(Product.id), nullable=False)
    receipt_id = Column(Integer, ForeignKey(Receipt.id), nullable=False)

    def __str__(self):
        return self.name


class Order(db.Model):  # phieu nhap hang
    id = Column(Integer, primary_key=True, autoincrement=True)
    order_date = Column(DateTime, default=datetime.now())
    user_id = Column(Integer, ForeignKey(User.id), nullable=False)
    order_detail = relationship('OrderDetails', backref='order', lazy=True)

    def __str__(self):
        return self.name


class OrderDetails(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    product_id = Column(Integer, ForeignKey(Product.id), nullable=False)
    order_id = Column(Integer, ForeignKey(Order.id), nullable=False)
    order_quantity = Column(Integer, nullable=False)

    def __str__(self):
        return self.name


class Interaction(BaseModel):
    __abstract__ = True

    product_id = Column(Integer, ForeignKey(Product.id), nullable=False)
    user_id = Column(Integer,ForeignKey(User.id),nullable=False)


class Comment(Interaction):
    content = Column(String(255),nullable=False)
    created_date = Column(DateTime, default=datetime.now())


if __name__ == '__main__':
    with app.app_context():
        # db.create_all()

        # import hashlib
        # u = User(name="Admin1", username="admin", password=str(hashlib.md5('123456'.encode('utf-8')).hexdigest()),
        #          user_role=UserRoleEnum.ADMIN)
        # db.session.add(u)

        c1 = Category(name='Văn học')
        c2 = Category(name='Kinh dị')
        c3 = Category(name='Tiểu thuyết')
        c4 = Category(name='Kinh tế')
        c5 = Category(name='Ngoại ngữ')

        db.session.add(c1)
        db.session.add(c2)
        db.session.add(c3)
        db.session.add(c4)
        db.session.add(c5)

        a1 = Author(name="Dale Carnegie")
        a2 = Author(name="Paulo Coelho")
        a3 = Author(name="Foreign Language Teaching")
        a4 = Author(name="Thảo Trang")
        a5 = Author(name="Napoleon Hill")
        a6 = Author(name="Nguyễn Nhật Ánh")

        db.session.add(a1)
        db.session.add(a2)
        db.session.add(a3)
        db.session.add(a4)
        db.session.add(a5)
        db.session.add(a6)
        p1 = Product(name='Đắc nhân tâm', quantity=800, price=80000,
                     image='https://res.cloudinary.com/lenvo1202/image/upload/v1704524078/dac-nhan-tam_vwtcgr.jpg',
                     active=1, author_id=1, category_id=1)
        p2 = Product(name='Nghĩ giàu làm giàu', price=77000, category_id=4,
                     image='https://res.cloudinary.com/lenvo1202/image/upload/v1704524209/nghi-giau-lam-giau_sjigoo.jpg',
                     active=1,author_id=5)
        p3 = Product(name='Tết ở làng địa ngục', price=120000, category_id=2,
                     image='https://res.cloudinary.com/lenvo1202/image/upload/v1704609155/tet-o-lang-dia-nguc_pbyxn7.jpg',
                     active=1,author_id=4)
        p4 = Product(name='Cambridge Ietls', price=125000, category_id=5,
                     image='https://res.cloudinary.com/lenvo1202/image/upload/v1704609259/ietls_kubegw.jpg',
                     active=1,author_id=3)
        p5 = Product(name='Nhà giả kim', price=60000, category_id=3,
                     image='https://res.cloudinary.com/lenvo1202/image/upload/v1704609362/nha-gia-kim_j4gqk8.jpg',
                     active=1,author_id=2)
        p6 = Product(name='Có Hai Con Mèo Ngồi Bên Cửa Sổ', price=60000, category_id=3,
                     image='https://res.cloudinary.com/lenvo1202/image/upload/v1704731603/2-con-meo_bbmg8w.jpg',
                     active=1,author_id=6)
        # p7 = Product(name='Samsung Z flip 5', price=22000000, category_id=1,
        #              image='https://res.cloudinary.com/dxxwcby8l/image/upload/v1688179242/hclq65mc6so7vdrbp7hz.jpg')
        # p8 = Product(name='iPad Promax', price=35000000, category_id=2,
        #              image='https://res.cloudinary.com/dxxwcby8l/image/upload/v1688179242/hclq65mc6so7vdrbp7hz.jpg')
        # p9 = Product(name='Galaxy Tab S7', price=24000000, category_id=2,
        #              image='https://res.cloudinary.com/dxxwcby8l/image/upload/v1688179242/hclq65mc6so7vdrbp7hz.jpg')
        # p10 = Product(name='Note 20', price=20000000, category_id=1,
        #               image='https://res.cloudinary.com/dxxwcby8l/image/upload/v1688179242/hclq65mc6so7vdrbp7hz.jpg')

        db.session.add_all([p1,p2,p3,p4,p5])
        # , p6, p7, p8, p9, p10])

        db.session.commit()
