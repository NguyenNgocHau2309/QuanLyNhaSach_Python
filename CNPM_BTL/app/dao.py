from app.models import Product, User, Order, OrderDetails, ReceiptDetails, Receipt, Author, Category, \
    Quydinh, QuydinhDetail, Comment
from app import app, db
import hashlib
import cloudinary.uploader
from flask_login import current_user
from sqlalchemy import func


def load_categories():
    return Category.query.all()


def load_products(kw=None, cate_id=None, page=None):
    products = Product.query

    if kw:
        products = products.filter(Product.name.contains(kw))

    if cate_id:
        products = products.filter(Product.category_id.__eq__(cate_id))

    if page:
        page = int(page)  # ép về kiểu int
        page_size = app.config['PAGE_SIZE']
        start = (page - 1) * page_size  # vị trí bắt đầu
        return products.slice(start, start + page_size)  # lấy từ vị trí start đến n phần tử đã được xác định

    return products.all()


def get_user_by_id(id):
    return User.query.get(id)


def count_products():
    return Product.query.count()


def auth_user(username, password):
    password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())
    return User.query.filter(User.username.__eq__(username.strip()),
                             User.password.__eq__(password)).first()


# def load_users():
#     with open(os.path.join(app.root_path, "data/users.json"), encoding="utf-8") as f:
#         return json.load(f)


def add_user(name, username, password, avatar):
    password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())
    u = User(name=name, username=username, password=password)
    if avatar:  # if avatar !=null
        res = cloudinary.uploader.upload(avatar)
        print(res)
        u.avatar = res['secure_url']

    db.session.add(u)
    db.session.commit()


def add_receipt(cart):
    if cart:  # if cart != null
        r = Receipt(user=current_user)  # create receipt
        db.session.add(r)  # luu vao session

        for c in cart.values():
            d = ReceiptDetails(quantity=c['quantity'], price=c['price'],
                               receipt=r, product_id=c['id'])
            db.session.add(d)

        db.session.commit()


def count_products_by_cate():
    return db.session.query(Category.id, Category.name, func.count(Product.id)) \
        .join(Product, Product.id == Category.id, isouter=True).group_by(Category.id).all()


def revenue_stats(kw=None):
    query = db.session.query(Product.id, Product.name, func.sum(ReceiptDetails.price * ReceiptDetails.quantity)) \
        .join(ReceiptDetails, ReceiptDetails.product_id == Product.id)
    if kw:
        query = query.filter(Product.name.contains(kw))

    return query.group_by(Product.id).all()


def revenue_month_stats(year=2024):
    query = db.session.query(func.extract('month', Receipt.created_date),
                             func.sum(ReceiptDetails.quantity * ReceiptDetails.price)) \
        .join(ReceiptDetails, ReceiptDetails.receipt_id.__eq__(Receipt.id)) \
        .filter(func.extract('year', Receipt.created_date).__eq__(year)) \
        .group_by(func.extract('month', Receipt.created_date))
    return query.all()


def get_product_by_id(id):
    return Product.query.get(id)


def get_comments_by_product(product_id):
    return Comment.query.filter(Comment.product_id.__eq__(product_id)).all()


def add_comment(product_id, content):
    c = Comment(user=current_user, product_id=product_id, content=content)
    db.session.add(c)
    db.session.commit()

    return c


# def add_comment(product_id, content):
#     c = Comment(product_id=product_id, content=content, user=current_user)
#     db.session.add(c)
#     db.session.commit()

# return c

if __name__ == '__main__':
    with app.app_context():
        print(count_products_by_cate())
