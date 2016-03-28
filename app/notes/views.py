from flask import Blueprint, render_template, flash, redirect, url_for, g, jsonify, current_app, request, send_from_directory
from flask.ext.login import login_required
from app.lesson.models import Lesson, LessonStudent
from .forms import AddNoteForm, AdminAddNoteForm
from .models import Note, NoteVote
import time, os, json, base64, hmac, urllib.parse
from hashlib import sha1, md5
from app.auth.decorators import permission_required
from datetime import datetime
from app.models import Semester, KarmaPoints, DATABASE


notes_bp = Blueprint('notes_bp', __name__, url_prefix='/notes')


@notes_bp.route('/view/<lessonid>')
@login_required
def view(lessonid):
    """Route to display the notes listing for a particular lesson"""
    try:
        lesson = Lesson.get(Lesson.id == lessonid)
    except:
        flash('Id not found', 'error')
        return redirect(url_for('auth_bp.profile'))

    notes = Note.select().where(Note.lesson == lessonid).order_by(-Note.year, +Note.semester)
    semesters = set()
    for note in notes:
        semesters.add((note.year, note.semester))

    if g.user.has_permission('note_admin'):
        form = AdminAddNoteForm()
    else:
        form = AddNoteForm()

    return render_template('notes/notes_listing.html', lesson=lesson, notes=notes, semesters=sorted(semesters), form=form)


@notes_bp.route('/add-note/<lessonid>', methods=('POST', 'GET'))
@login_required
def add_note(lessonid):
    """Route to render AddNoteForm or process AddNoteForm to create a Note

    **NOTE: This does not actually upload the file to S3. That is done via AJAX.**

    """
    form = AddNoteForm()
    if form.validate_on_submit():
        # TODO: Add error handling
        filename = form.filename.data
        month = datetime.now().month
        semester = Semester.current_semester()
        print(form.file.data)
        note = Note.create(
            filename=filename,
            s3_filename=form.file_hash.data,
            uploader=g.user.user_id,
            description=form.description.data,
            lesson=lessonid,
            semester=semester.value,
            year=datetime.now().year,
            original_filename=form.file.data.filename)
        g.user.karma_points += KarmaPoints.upload_note.value
        g.user.save()

        return redirect(url_for(".view", lessonid=lessonid))
    return render_template('notes/add_note.html', form=form)


@notes_bp.route('/sign_s3/')
def sign_s3():
    """Route to sign a note for upload to S3. Accessed via AJAX"""
    AWS_ACCESS_KEY = os.environ['AWS_ACCESS_KEY']
    AWS_SECRET_KEY = os.environ['AWS_SECRET_KEY']
    S3_BUCKET = os.environ['S3_BUCKET']

    filename = request.args.get('file_name')
    filename_hash = md5(bytes(g.user.email + filename, 'utf-8')).hexdigest()
    i = 0
    while Note.select().where(Note.s3_filename == filename_hash).exists():
        filename_hash = md5(bytes(g.user.email + filename + str(i), 'utf-8')).hexdigest()
        i += 1

    object_name = urllib.parse.quote_plus(filename_hash)
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
        'file_hash': filename_hash
    })
    return content


# @notes_bp.route("/vote/<noteid>/<upvote>")
# @login_required
# def vote(noteid, upvote):
#     """Route to allow a user to vote on a note"""
#     # TODO: Move to POST request
#     note = Note.get(Note.id == noteid)
#     has_upvoted = note.has_upvoted(g.user)
#     has_voted = note.has_voted(g.user)
#     vote = True if upvote == "1" else False
#     if has_upvoted and vote:
#         return jsonify({'success': False, 'message': "Error! You have already upvoted this note!"})
#     elif has_voted and not has_upvoted and not vote:
#         return jsonify({'success': False, 'message': "Error! You have already downvoted this note!"})
#     else:
#         success, message = note.vote(g.user, vote)
#         if success:
#             if not has_voted:
#                 g.user.karma_points += KarmaPoints.note_vote.value
#                 g.user.save()
#
#         return jsonify({'success': success, 'message': message})

@notes_bp.route("/vote/<noteid>")
@login_required
def vote(noteid):
    """Route to allow a user to vote on a note"""
    # TODO: Move to POST request
    note = Note.get(Note.id == noteid)

    has_voted = note.has_voted(g.user)

    upvote = True

    if has_voted:
        upvote = not note.has_upvoted(g.user)

    success, message = note.vote(g.user, upvote)
    if success:
        if not has_voted:
            g.user.karma_points += KarmaPoints.note_vote.value
            g.user.save()

    return jsonify({'success': success, 'numberOfVotes': note.votes, 'message': message})

@notes_bp.route('/add-admin-note/<lessonid>', methods=('POST', 'GET'))
@login_required
@permission_required('note_admin')
def add_admin_note(lessonid):
    """Route to allow users with the note_admin permission to upload notes with specific years and semesters"""
    form = AdminAddNoteForm()
    if form.validate_on_submit():
        # TODO: Add error handling
        note = Note.create(
            filename=form.filename.data,
            s3_filename=form.file_hash.data,
            uploader=g.user.user_id,
            description=form.description.data,
            lesson=lessonid,
            semester=int(form.semester.data),
            year=form.year.data,
            original_filename=form.file.data.filename)
        g.user.karma_points += KarmaPoints.upload_note.value
        g.user.save()

        return redirect(url_for(".view", lessonid=lessonid))
    return render_template('notes/add_note.html', form=form)