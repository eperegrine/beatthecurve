from flask import Flask, g, render_template
from flask.ext.login import LoginManager, current_user
from peewee import DoesNotExist
from .models import DATABASE
from .auth.models import User
import os
from app.notes.models import Semester

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hufenaifneianwdawaffioawnfiohaewifs'
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config["DEBUG"] = True

from app.models import DATABASE
from app.auth.models import School, User, Permission, UserPermission
from app.lesson.models import Lesson, LessonStudent
from app.notes.models import Lecture, Discussion, Note, NoteVote
from app.qa.models import Question, Reply
from app.exams.models import Exam, ExamVote
from app.studygroups.models import StudyGroup, StudyGroupComment, StudyGroupMembers, StudyGroupSession
from app.search.models import Option, UserOption

DATABASE.create_tables([School, User, Permission, UserPermission, Lesson, LessonStudent, Lecture, Discussion, Note,
                        NoteVote, Question, Reply, Exam, ExamVote, StudyGroup, StudyGroupComment, StudyGroupMembers,
                        StudyGroupSession, Option, UserOption], safe=True)

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
    return dict(semester_enum=dict(list(map(lambda x: [x.value, x.name], Semester))))

@app.route('/')
def index():
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

from app.lesson.models import LessonStudent
app.jinja_env.globals.update(get_lessons=LessonStudent.get_attended_lessons)
