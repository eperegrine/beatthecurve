from flask import Flask, g
from flask.ext.login import LoginManager, current_user
from .models import DATABASE
from .auth.models import User

app = Flask(__name__)

# Set up login manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


# Login Manager Functions

@login_manager.user_loader
def load_user(userid):
    try:
        return User.get(User.id == userid)
    except:
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