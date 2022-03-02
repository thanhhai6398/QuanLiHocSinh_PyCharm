from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:123456@localhost/qlhs?charset=utf8mb4"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
app.secret_key = "$!@$@$^$%%*^&)!@#Nhom11"

db = SQLAlchemy(app=app)
login_manager = LoginManager(app=app)
login_manager.init_app(app)

endpoint = "https://test-payment.momo.vn/v2/gateway/api/create"
partnerCode = "MOMONTKI20211108"
accessKey = "XDzcVUiDzu1nzzyR"
secretKey = "fOvRUtoRKrHVgHuY7QNk68XD7THt9yBp"
redirectUrl = "http://127.0.0.1:5000/ketquathanhtoan"
ipnUrl = "http://127.0.0.1:5000/api/xlketquathanhtoan"
requestType = "captureWallet"

#STMP Config
port = 465  # For SSL
password = "hiimkq0901"