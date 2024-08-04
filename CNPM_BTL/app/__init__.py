from flask import Flask
from urllib.parse import quote
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from urllib.parse import quote # chứa ký tự đặc biệt trong password mysql
import cloudinary
app = Flask(__name__)


app.secret_key = '^%*&^^HJGHJGHJFD%^&%&*^*(^^^&^(*^^$%^GHJFGHJH'
app.config["SQLALCHEMY_DATABASE_URI"] = 'mysql+pymysql://root:%s@localhost/qlnhasach3' % quote('Admin@123')
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
app.config["PAGE_SIZE"] = 6
db = SQLAlchemy(app=app)
login = LoginManager(app=app)

cloudinary.config(
    cloud_name="lenvo1202",
    api_key="493287268151437",
    api_secret="nMqfQqWtd7VFbrYFC8YmNK-9X4o"
)

