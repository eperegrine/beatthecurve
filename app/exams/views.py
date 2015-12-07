from flask import Blueprint, render_template, flash, redirect, url_for
from flask.ext.login import login_required
from app.lesson.models import Lesson

exams_bp = Blueprint('exams_bp', __name__, url_prefix='/exams')


@exams_bp.route('/view/<lessonid>')
@login_required
def view(lessonid):
    # TODO: Validate id
    try:
        lesson = Lesson.get(Lesson.id == lessonid)
    except:
        flash('Id not found')
        return redirect(url_for('auth_bp.profile'))
    return render_template('exams/exam_listing.html', lesson=lesson)
