import math

from flask import render_template, request, redirect, session, jsonify, url_for
import dao
import utils
from app import app, login
from flask_login import login_user, logout_user, login_required
from functools import wraps


@app.route('/')
def index():
    kw = request.args.get('kw')

    cate_id = request.args.get('cate_id')
    # cate = dao.load_categories()
    page = request.args.get('page')
    total = dao.count_products()  # total products trên database
    pages = app.config["PAGE_SIZE"]  # amount on 1 page
    products = dao.load_products(kw=kw, cate_id=cate_id, page=page)
    #
    return render_template('index.html', products=products,
                           pages=math.ceil(total / app.config['PAGE_SIZE']))  # amount on 1 page


@app.route('/all')
def view_all():
    kw = request.args.get('kw')

    cate_id = request.args.get('cate_id')
    # cate = dao.load_categories()
    page = request.args.get('page')
    total = dao.count_products()  # total products trên database
    pages = app.config["PAGE_SIZE"]  # amount on 1 page
    products = dao.load_products(kw=kw, cate_id=cate_id, page=page)
    #
    return render_template('all.html', products=products,
                           pages=math.ceil(total / app.config['PAGE_SIZE']))  # amount on 1 page


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get("user"):
            return redirect(url_for('index', next=request.url))
        return f(*args, **kwargs)
    return decorated_function


# @app.route('/admin/login', methods=['post'])
# def admin_login():
#      = request.form.get('username')
#      request.form.get('password')
#
#     user= dao.auth_user(username=username,password=password)
#     if user: # khác null
#         login_user(user=user)
#     return redirect('/admin')
@login.user_loader
def get_user(user_id):
    return dao.get_user_by_id(user_id)


@app.route('/api/cart', methods=['post'])
def add_cart():
    cart = session.get('cart')  # Lấy giỏ
    if cart is None:  # check có giỏ chưa
        cart = {}

    data = request.json
    id = str(data.get('id'))

    if id in cart:  # product đã có trong giỏ
        cart[id]["quantity"] = cart[id]["quantity"] + 1
    else:  # product chưa có trong giỏ
        cart[id] = {
            "id": id,
            "name": data.get('name'),
            "price": data.get('price'),
            "quantity": 1
        }
    # lưu vô session
    session['cart'] = cart

    return jsonify(utils.count_cart(cart))


@app.route('/cart')
def cart_list():
    return render_template('cart.html')


@app.context_processor  # gắn tất cả response => category: Mobile, Tablet lên header
def common_res():
    return {
        'categories': dao.load_categories(),
        'cart': utils.count_cart(session.get('cart'))
    }


@app.route('/api/cart/<product_id>', methods=['put'])
def update_cart(product_id):
    cart = session.get('cart')  # Lấy giỏ
    if cart and product_id in cart:
        quantity = request.json.get('quantity')
        cart[product_id]['quantity'] = int(quantity)  # lấy trường quantity của product = quantity mới bỏ lên

    session['cart'] = cart  # update lại lên session

    return jsonify(utils.count_cart(cart))


@app.route('/api/cart/<product_id>', methods=['delete'])
def delete_cart(product_id):
    cart = session.get('cart')  # Lấy giỏ
    if cart and product_id in cart:
        del cart[product_id]

    session['cart'] = cart  # update lại lên session

    return jsonify(utils.count_cart(cart))


@app.route('/products/<id>')
def details(id):
    comments = dao.get_comments_by_product(id)
    return render_template('details.html', product=dao.get_product_by_id(id), comments=comments)


@app.route('/api/product/<id>/comments', methods=['post'])
@login_required
def add_comment(id):
    try:
        c = dao.add_comment(product_id=id, content=request.json.get('content'))
    except Exception as ex:
        print(ex)
        return jsonify({'status': 500, 'err_msg': "..."})
    else:
        return jsonify({'status': 200, 'comment': {'content': c.content,
                                                   'created_date': c.created_date,
                                                   'user': {'avatar': c.user.avatar}}})


# @app.route("/login-admin", methods=['GET', 'POST'])
# def login_admin():
#     if request.method == 'POST':
#     username = request.form.get("username")
#     password = request.form.get("password")
#     user = User.query.filter(username == username,
#             password == password).first()
#     if user:
#         login_user(user=user)
#     return redirect("/admin")


@app.route("/login", methods=['get', 'post'])
def login_user_process():
    if request.method.__eq__('POST'):
        username = request.form.get('username')
        password = request.form.get('password')

        user = dao.auth_user(username=username, password=password)
        if user:  # != null
            login_user(user=user)

        next = request.args.get('next')
        return redirect("/" if next is None else next)

    return render_template('login.html')


@app.route('/logout')
def process_logout_user():
    logout_user()
    return redirect("/login")


@app.route('/register', methods=["get", "post"])
def register_user():
    err_msg = ""
    if request.method.__eq__('POST'):
        password = request.form.get('password')
        confirm = request.form.get('confirm')
        # if password.strip().__eq__(confirm.strip()):  # nếu mk != confirm
        if password.__eq__(confirm):
            try:
                dao.add_user(name=request.form.get('name'),
                             username=request.form.get('username'),
                             password=password,
                             avatar=request.files.get('avatar'))
            except:
                err_msg = "Hệ thống bị lỗi"
            else:
                return redirect('/login')
        else:
            err_msg = "Mật khẩu chưa trùng khớp"
    return render_template('register.html', err_msg=err_msg)


# @app.route('/registerByAdmin', methods=["get", "post"])
# def register_user_bya():
#     err_msg = ""
#     if request.method.__eq__('POST'):
#         password = request.form.get('password')
#         confirm = request.form.get('confirm')
#
#         # if password.strip().__eq__(confirm.strip()):  # nếu mk != confirm
#         if password.__eq__(confirm):
#             try:
#                 dao.add_user(name=request.form.get('name'),
#                              username=request.form.get('username'),
#                              password=password,
#                              userrole = request.form.get('user_role'),
#                              avatar=request.files.get('avatar'))
#             except:
#                 err_msg = "Hệ thống bị lỗi"
#             else:
#                 return redirect('/login')
#         else:
#             err_msg = "Mật khẩu chưa trùng khớp"
#     return render_template('registerByAdmin.html', err_msg=err_msg)


@app.route('/admin/login', methods=['post'])
def admin_login():
    username = request.form.get('username')
    password = request.form.get('password')

    user = dao.auth_user(username=username, password=password)
    if user:  # khác null
        login_user(user=user)
    return redirect('/admin')


@app.route('/api/pay', methods=['post'])
def pay():
    try:
        dao.add_receipt(session.get('cart'))
    except:
        return jsonify({'status': 500, 'err_msg': 'Hệ thống đang lỗi'})
    else:
        del session['cart']
        return jsonify({'status': 200})


# @app.errorhandler(404)
# def page_not_found(error):
#     return render_template('page_not_found.html'), 404


if __name__ == '__main__':
    from app import admin

    app.run(debug=True)  # print lỗi ra
