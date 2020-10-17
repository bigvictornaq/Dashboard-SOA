from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
import cloudinary as cloud
from flask_email import Mail

app = Flask(__name__)
app.config['SECRET_KEY'] = '8d723bc78222badb938f27312dde8956'
app.config['SQLALCHEMY_DATABASE_URI'] = "postgres://ifxvfpua:4552V0r2IkVujztnh3F5puUE79kTmuQM@lallah.db.elephantsql.com:5432/ifxvfpua"

#Configuracion del API IMAGE STORAGE
cloud.config(
        cloud_name ="pixies",
        api_key = "325945932269836",
        api_secret = "7sVtJrQrKypYez-2Jch0hrJeXAY"
)

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'index'
login_manager.login_message_category = 'warning'
app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True

from cat_web import routes