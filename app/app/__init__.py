from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from urllib.parse import quote


appdemo = Flask(__name__)
appdemo.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:%s@localhost/appdb?charset=utf8mb4" %quote("Admin@123")
appdemo.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True

db = SQLAlchemy(appdemo)