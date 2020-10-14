from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager


app = Flask(__name__)
app.config['SECRET_KEY'] = '8d723bc78222badb938f27312dde8956'
app.config['SQLALCHEMY_DATABASE_URI'] = "postgres://ifxvfpua:4552V0r2IkVujztnh3F5puUE79kTmuQM@lallah.db.elephantsql.com:5432/ifxvfpua"

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'index'
login_manager.login_message_category = 'warning'

from cat_web import routes