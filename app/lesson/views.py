from flask import Blueprint, g, render_template, flash, redirect, url_for
from flask.ext.login import login_required
from .forms import AttendLessonsForm
from .models import Lesson, LessonStudent

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
        # TODO: Change redirect
        return redirect(url_for('index'))

    return render_template('lesson/add.html', form=form)