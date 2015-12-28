from flask import Blueprint, render_template, flash, redirect, url_for, g, jsonify, current_app, request, send_from_directory
from flask.ext.login import login_required
from app.lesson.models import Lesson, LessonStudent
from .forms import AddLectureForm, AddNoteForm, AddDiscussionForm
from .models import Lecture, Discussion, Note, Semester
import time, os, json, base64, hmac, urllib.parse
from hashlib import sha1
from app.auth.decorators import permission_required


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
    lectures = [lecture for lecture in Lecture.select().where((Lecture.lesson_id == lesson.id)).order_by(Lecture.year)]
    print(lectures)
    notes = {}
    semesters = set()
    for lecture in lectures:
        semesters.add((lecture.year, lecture.semester))
        query = Note.select().where(Note.lecture == lecture.id)
        notes[lecture.id] = [note for note in query]
    print(notes)
    return render_template('notes/notes_listing.html', lesson=lesson, lectures=lectures, notes=notes, semesters=sorted(semesters))


@notes_bp.route('/add-lecture', methods=('POST', 'GET'))
@login_required
@permission_required('lecture_admin')
def add_lecture():
    # TODO: Validate user is attending lesson
    form = AddLectureForm()
    form.lesson.choices = [(str(lesson.id), lesson.lesson_name) for lesson in
                           LessonStudent.get_attended_lessons(g.user.user_id)]
    print(form.year.choices)
    print(form.year.data)
    if form.validate_on_submit():
        try:
            lecture = Lecture.create(
                lesson_id=int(form.lesson.data),
                name=form.name.data,
                year=form.year.data,
                semester=form.semester.data
            )
            flash('Success')
            return redirect(url_for('auth_bp.profile'))
        except Exception as e:
            print(e)
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
    form.lecture.choices = [(str(lecture.id), lecture.name + " - " + Semester(lecture.semester).name + " " + str(lecture.year)) for lecture in
                            Lecture.select().where(Lecture.lesson_id == int(lessonid))]
    print(form.discussion.data)
    if form.lecture.data == 'None' and request.method == 'GET':
        form.discussion.choices = [('-1', '')]
    else:
        form.discussion.choices = [(str(discussion.id), discussion.name) for discussion in Discussion.select().where(Discussion.lecture_id == form.lecture.data)]

    if form.validate_on_submit():
        # TODO: Add error handling
        # Upload file
        filename = form.file.data.filename
        if form.discussion.data == 'None':
            note = Note.create(filename=filename, uploader=g.user.user_id, lecture=form.lecture.data)
        else:
            note = Note.create(filename=filename, uploader=g.user.user_id, lecture=form.lecture.data, discussion=form.discussion.data)
        lecture = Lecture.get(Lecture.id == form.lecture.data)
        lecture.number_of_files += 1
        lecture.save()
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
@permission_required('discussion_admin')
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


@notes_bp.route('/sign_s3/')
def sign_s3():
    AWS_ACCESS_KEY = 'AKIAJPAM7ZQCRQQ5GP3Q'
    AWS_SECRET_KEY = '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'
    S3_BUCKET = 'beatthecurve'

    object_name = urllib.parse.quote_plus(request.args.get('file_name'))
    mime_type = request.args.get('file_type')

    expires = int(time.time()+60*60*24)
    amz_headers = "x-amz-acl:public-read"

    string_to_sign = "PUT\n\n%s\n%d\n%s\n/%s/notes/%s" % (mime_type, expires, amz_headers, S3_BUCKET, object_name)

    signature = base64.encodebytes(hmac.new(AWS_SECRET_KEY.encode(), string_to_sign.encode('utf8'), sha1).digest())
    signature = urllib.parse.quote_plus(signature.strip())

    url = 'https://s3-us-west-2.amazonaws.com/%s/notes/%s' % (S3_BUCKET, object_name)

    content = json.dumps({
        'signed_request': '%s?AWSAccessKeyId=%s&Expires=%s&Signature=%s' % (url, AWS_ACCESS_KEY, expires, signature),
        'url': url,
    })
    return content


@notes_bp.route('/detail/<noteid>')
@login_required
def detail(noteid):
    try:
        note = Note.get(Note.id == noteid)
    except:
        flash("Invalid note")
        return redirect(url_for("auth_bp.profile"))
    return render_template("notes/detail.html", note=note)


@notes_bp.route("/vote/<noteid>/<upvote>")
@login_required
def vote(noteid, upvote):
    note = Note.get(Note.id == noteid)
    has_upvoted = note.has_upvoted(g.user)
    has_voted = note.has_voted(g.user)
    vote = True if upvote == "1" else False
    if has_upvoted and vote:
        flash("Error! You have already upvoted this note!")
    elif has_voted and not has_upvoted and not vote:
        flash("Error! You have already downvoted this note!")
    else:
        success, message = note.vote(g.user, vote)
        if success:
            flash("Success")
        else:
            flash(message)
    print(note.lecture.lesson_id)
    return redirect(url_for(".view", lessonid=note.lecture.lesson_id.id))
