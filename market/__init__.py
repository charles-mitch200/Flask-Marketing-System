from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///market1.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = '714969a337ceae7bec39671e'

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
# Specify where the login route is located, for the login_required to authorize the route
login_manager.login_view = "login_page"
# Assign a category to the login_required alert
login_manager.login_message_category = "info"

from market import routes

app.app_context().push()