from flask import Blueprint, g, render_template, flash, redirect, url_for
from flask.ext.login import login_required
from .forms import AttendLessonsForm, CreateLessonForm
from .models import Lesson, LessonStudent
from app.search.models import UserOption
from app.auth.decorators import permission_required

lesson_bp = Blueprint('lesson_bp', __name__, url_prefix='/lessons')


@lesson_bp.route('/add', methods=('POST', 'GET'))
@login_required
def add():
    form = AttendLessonsForm()
    form.lessons.choices = [(str(lesson.id), lesson.lesson_name + " - " + lesson.professor) for lesson in Lesson.get_unattended_lessons(g.user.user_id, g.user.school_id)]

    if form.validate_on_submit():
        lesson_ids = [int(id) for id in form.lessons.data]
        LessonStudent.attend(g.user.user_id, lesson_ids)
        flash("Added!")

        if UserOption.select().where(UserOption.user == g.user.user_id).exists():
            return redirect(url_for('auth_bp.profile'))
        else:
            return redirect(url_for("search_bp.options"))

    return render_template('lesson/add.html', form=form)


@lesson_bp.route('/create', methods=('POST', 'GET'))
@login_required
@permission_required('lesson_admin')
def create():
    form = CreateLessonForm()
    form.school.data = g.user.school_id

    if form.validate_on_submit():
        Lesson.create(
            lesson_name=form.name.data,
            professor=form.professor.data,
            school_id=g.user.school_id
        )
        return redirect(url_for("auth_bp.profile"))

    return render_template('lesson/create.html', form=form)
