from flask import Flask, g
from flask.ext.login import LoginManager, current_user
from peewee import DoesNotExist
from .models import DATABASE
from .auth.models import User

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hufenaifneianwdawaffioawnfiohaewifs'

# Set up login manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


# Login Manager Functions

@login_manager.user_loader
def load_user(user_id):
    try:
        return User.get(User.user_id == user_id)
    except DoesNotExist:
        return None


# Before and After request functions
@app.before_request
def before_request():
    """Connect to database before each request"""
    g.db = DATABASE
    g.db.connect()
    g.user = current_user


@app.after_request
def after_request(response):
    """Close the database connection after each response"""
    g.db.close()
    return response

from app.auth.views import auth_bp
app.register_blueprint(auth_bp)