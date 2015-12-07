from flask import Flask, g, render_template
from flask.ext.login import LoginManager, current_user
from peewee import DoesNotExist
from .models import DATABASE
from .auth.models import User

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hufenaifneianwdawaffioawnfiohaewifs'

from app.models import DATABASE
from app.auth.models import School, User
from app.lesson.models import Lesson, LessonStudent

DATABASE.create_tables([School, User, Lesson, LessonStudent], safe=True)

# Set up login manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth_bp.login'


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


@app.route('/')
def index():
    return render_template('layout.html')


@app.route('/notes')
def notes():
    return render_template('notes/notes_listing.html')


@app.route('/qa')
def qa():
    return render_template('qa/qa_listing.html')


@app.route('/exams')
def exams():
    return render_template('exams/exam_listing.html')


@app.route('/studygroups')
def study_groups():
    return render_template('studygroups/study_groups_listing.html')


from app.auth.views import auth_bp
app.register_blueprint(auth_bp)

from app.lesson.views import lesson_bp
app.register_blueprint(lesson_bp)

from app.lesson.models import LessonStudent
app.jinja_env.globals.update(get_lessons=LessonStudent.get_attended_lessons)
