from flask import Flask
from flask_sqlalchemy import SQLAlchemy



app = Flask(__name__)
app.config['SECRET_KEY'] = '8d723bc78222badb938f27312dde8956'
app.config['SQLALCHEMY_DATABASE_URI'] = "postgres://ifxvfpua:4552V0r2IkVujztnh3F5puUE79kTmuQM@lallah.db.elephantsql.com:5432/ifxvfpua"

db = SQLAlchemy(app)

from cat_web import routes