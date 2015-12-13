from flask import Blueprint, render_template, flash, redirect, url_for, g, jsonify, current_app, request, send_from_directory
from flask.ext.login import login_required
from app.lesson.models import Lesson, LessonStudent
from .forms import AddLectureForm, AddNoteForm, AddDiscussionForm
from .models import Lecture, Discussion, Note
from werkzeug.utils import secure_filename
import os

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


@notes_bp.route('/add-lecture', methods=('POST', 'GET'))
@login_required
def add_lecture():
    # TODO: Validate user is attending lesson
    form = AddLectureForm()
    form.lesson.choices = [(str(lesson.id), lesson.lesson_name) for lesson in
                           LessonStudent.get_attended_lessons(g.user.user_id)]

    if form.validate_on_submit():
        try:
            lecture = Lecture.create(
                lesson_id=int(form.lesson.data),
                name=form.name.data
            )
            os.makedirs(os.path.join(current_app.config['UPLOAD_FOLDER'], "notes", form.lesson.data, lecture.id))
            flash('Success')
            return redirect(url_for('auth_bp.profile'))
        except:
            # TODO: Improve exception handling
            flash('There was an error')

    return render_template('notes/add_lecture.html', form=form)


@notes_bp.route('/get-discussions/<lectureid>')
@login_required
def get_discussions(lectureid):
    # TODO: Validate lectureid
    discussion = [(str(discussion.id), discussion.name) for discussion in Discussion.select().where(Discussion.lecture_id == lectureid)]
    json = jsonify(discussion)
    return json


@notes_bp.route('/add-note/<lessonid>', methods=('POST', 'GET'))
@login_required
def add_note(lessonid):
    form = AddNoteForm()
    form.lecture.choices = [(str(lecture.id), lecture.name) for lecture in
                            Lecture.select().where(Lecture.lesson_id == int(lessonid))]
    print(form.discussion.data)
    if form.lecture.data == 'None' and request.method == 'GET':
        form.discussion.choices = [('-1', '')]
    else:
        form.discussion.choices = [(str(discussion.id), discussion.name) for discussion in Discussion.select().where(Discussion.lecture_id == form.lecture.data)]

    if form.validate_on_submit():
        # TODO: Add error handling
        # Upload file
        filename = secure_filename(form.file.data.filename)
        filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], "notes", lessonid, form.lecture.data, filename)
        file = request.files[form.file.name]
        file.save(filepath)
        # Create model
        if form.discussion.data == 'None':
            note = Note.create(filename=filename, uploader=g.user.user_id, lecture=form.lecture.data)
        else:
            note = Note.create(filename=filename, uploader=g.user.user_id, lecture=form.lecture.data, discussion=form.discussion.data)
        return redirect(url_for(".view", lessonid=lessonid))
    return render_template('notes/add_note.html', form=form)


@notes_bp.route('/uploads/<lessonid>/<lectureid>/<noteid>', methods=['GET', 'POST'])
def download(lessonid, lectureid, noteid):
    filename = Note.get(Note.id == noteid).filename
    uploads = os.path.join(os.getcwd(), current_app.config['UPLOAD_FOLDER'], "notes", lessonid, lectureid)
    print(uploads)
    return send_from_directory(uploads, filename)


@notes_bp.route('/add-discussion/<lessonid>', methods=('POST', 'GET'))
@login_required
def add_discussion(lessonid):
    form = AddDiscussionForm()
    form.lecture.choices = [(str(lecture.id), lecture.name) for lecture in
                            Lecture.select().where(Lecture.lesson_id == int(lessonid))]

    if form.validate_on_submit():
        Discussion.create(
            lecture_id=form.lecture.data,
            name=form.name.data
        )
        flash('Success')
        return redirect(url_for(".view", lessonid=lessonid))

    return render_template('notes/add_discussion.html', form=form)
