from flask import Blueprint, render_template, flash, redirect, url_for, g
from flask.ext.login import login_required
from app.lesson.models import Lesson, LessonStudent
from .forms import AddLectureForm
from .models import Lecture

notes_bp = Blueprint('notes_bp', __name__, url_prefix='/notes')


@notes_bp.route('/view/<lessonid>')
@login_required
def view(lessonid):
    # TODO: Validate id
    try:
        lesson = Lesson.get(Lesson.id == lessonid)
    except:
        flash('Id not found')
        return redirect(url_for('auth_bp.profile'))
    lectures = [lecture for lecture in Lecture.select().where(Lecture.lesson_id == lesson.id)]
    print(lectures)
    notes = {}
    for lecture in lectures:
        notes[lecture.id] = [] # TODO: Modify to actually get files
    return render_template('notes/notes_listing.html', lesson=lesson, lectures=lectures, notes=notes)


@notes_bp.route('/add-lecture', methods=('POST', 'GEt'))
@login_required
def add_lecture():
    # TODO: Validate user is attending lesson
    form = AddLectureForm()
    form.lesson.choices = [(str(lesson.id), lesson.lesson_name) for lesson in
                           LessonStudent.get_attended_lessons(g.user.user_id)]

    if form.validate_on_submit():
        try:
            Lecture.create(
                lesson_id=int(form.lesson.data),
                name=form.name.data
            )
            flash('Success')
            return redirect(url_for('auth_bp.profile'))
        except:
            # TODO: Improve exception handling
            flash('There was an error')

    return render_template('notes/add_lecture.html', form=form)
