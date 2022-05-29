#This file is used for initialising certain inbuilt functions from libraries for the ease of use in the subsequent files.


import bcrypt
from flask import Flask 
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///about.db'
db = SQLAlchemy(app)

bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = "login_page"
login_manager.login_message_category = "info"
app.config['SECRET_KEY'] = '1a476a28f0583c68e05c02c0'
from Recommendation import routes