from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from urllib.parse import quote
from flask_login import LoginManager

appdemo = Flask(__name__)
appdemo.secret_key = "390riuriewh38479832infu9yf9wehihfweyr83ur8weoru$$$%#$#$^##^$#"
appdemo.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:%s@localhost/appdb?charset=utf8mb4" %quote("Admin@123")
appdemo.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
appdemo.config["PAGE_SIZE"] = 4

db = SQLAlchemy(app=appdemo)

login = LoginManager(app=appdemo)