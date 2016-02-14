import eventlet
eventlet.monkey_patch()

from flask import Flask, g, render_template
from flask.ext.login import LoginManager, current_user
from peewee import DoesNotExist
from .models import DATABASE, Semester
from .auth.models import User
import os
import sendgrid
import peewee

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hufenaifneianwdawaffioawnfiohaewifs' # TODO: Move to environment variable
app.config['UPLOAD_FOLDER'] = 'uploads' # TODO: Check if can be removed
app.config["DEBUG"] = True
app.config["PRESERVE_CONTEXT_ON_EXCEPTION"] = False

sg = sendgrid.SendGridClient(os.environ['SENDGRID_KEY'])

from app.models import DATABASE
from app.auth.models import School, User, Permission, UserPermission
from app.lesson.models import Lesson, LessonStudent
from app.notes.models import Lecture, Discussion, Note, NoteVote
from app.qa.models import Question, Reply
from app.exams.models import Exam, ExamVote
from app.studygroups.models import StudyGroup, StudyGroupComment, StudyGroupMembers, StudyGroupSession
from app.search.models import Option, UserOption
from app.chat.models import Message

# Print all queries to stderr.
import logging
logger = logging.getLogger('peewee')
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.StreamHandler())

tables = [School, User, Permission, UserPermission, Lesson, LessonStudent, Lecture, Discussion, Note,
                        NoteVote, Question, Reply, Exam, ExamVote, StudyGroup, StudyGroupComment, StudyGroupMembers,
                        StudyGroupSession, Option, UserOption, Message]
for table in tables:
    print(table)
    try:
        table.create_table()
    except peewee.ProgrammingError:
        continue

# Set up login manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth_bp.login'


# Login Manager Functions

@login_manager.user_loader
def load_user(user_id):
    """Returns a User matching the supplied user_id or None for Flask-Login"""
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

# Environment has STATIC_URL='http://my_s3_bucket.aws.amazon.com/'
@app.context_processor
def inject_static_url():
    """
    Inject the variable 'static_url' into the templates. Grab it from
    the environment variable STATIC_URL, or use the default.

    Template variable will always have a trailing slash.

    """
    static_url = os.environ.get('STATIC_URL', app.static_url_path)
    if not static_url.endswith('/'):
        static_url += '/'
    return dict(
        static_url=static_url
    )


@app.context_processor
def inject_semester_enum():
    """Inject the app.models.Semester enum into templates"""
    return dict(semester_enum=dict(list(map(lambda x: [x.value, x.name], Semester))))


@app.route('/')
def index():
    """Route to display root homepage"""
    return render_template('index.html')

from app.auth.views import auth_bp
app.register_blueprint(auth_bp)

from app.lesson.views import lesson_bp
app.register_blueprint(lesson_bp)

from app.notes.views import notes_bp
app.register_blueprint(notes_bp)

from app.qa.views import qa_bp
app.register_blueprint(qa_bp)

from app.exams.views import exams_bp
app.register_blueprint(exams_bp)

from app.studygroups.views import studygroups_bp
app.register_blueprint(studygroups_bp)

from app.search.views import search_bp
app.register_blueprint(search_bp)

from app.chat.views import chat_bp
app.register_blueprint(chat_bp)

from app.lesson.models import LessonStudent
app.jinja_env.globals.update(get_lessons=LessonStudent.get_attended_lessons)
