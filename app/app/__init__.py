from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from urllib.parse import quote
from flask_login import LoginManager
import cloudinary
from flask_babel import Babel

#file nay de cau hinh cac thong tin ket noi

appdemo = Flask(__name__)
appdemo.secret_key = "390riuriewh38479832infu9yf9wehihfweyr83ur8weoru$$$%#$#$^##^$#"
appdemo.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:%s@localhost/appdb?charset=utf8mb4" %quote("Admin@123")
appdemo.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
appdemo.config["PAGE_SIZE"] = 4
appdemo.config["CART_KEY"] = "cart"

cloudinary.config(cloud_name="dcee16rsp",
                  api_key="645857166697866",
                  api_secret="QpsoRSYSM8S4rzFOS51f3615UmQ")

db = SQLAlchemy(app=appdemo)

login = LoginManager(app=appdemo)

def get_locale():
     return "vi"

babel = Babel(app=appdemo, locale_selector=get_locale)

