from flask import Blueprint, render_template, flash, redirect, url_for, request, g
from flask.ext.login import login_required
from .forms import AddExamForm
from .models import Exam
from app.lesson.models import Lesson
import urllib.parse
import time
import base64
import hmac
import json
import os
from hashlib import sha1, md5
from app.models import KarmaPoints

exams_bp = Blueprint('exams_bp', __name__, url_prefix='/exams')


@exams_bp.route('/view/<lessonid>')
@login_required
def view(lessonid):
    """Route that lists the exams for a lesson"""
    try:
        lesson = Lesson.get(Lesson.id == lessonid)
    except:
        flash('Id not found', 'error')
        return redirect(url_for('auth_bp.profile'))
    exams = Exam.select().where(Exam.lesson == lessonid)
    semesters = set()
    for exam in exams:
        semesters.add((exam.year, exam.semester))
    print(semesters)
    form = AddExamForm()

    return render_template('exams/exam_listing.html', lesson=lesson, exams=exams, semesters=sorted(semesters), form=form)


@exams_bp.route('/sign_s3/')
def sign_s3():
    """Route to sign files for upload to S3. Accessed via AJAX."""
    AWS_ACCESS_KEY = os.environ['AWS_ACCESS_KEY']
    AWS_SECRET_KEY = os.environ['AWS_SECRET_KEY']
    S3_BUCKET = os.environ['S3_BUCKET']

    filename = request.args.get('file_name')
    filename_hash = md5(bytes(g.user.email + filename, 'utf-8')).hexdigest()
    i = 0
    while Exam.select().where(Exam.s3_filename == filename_hash).exists():
        filename_hash = md5(bytes(g.user.email + filename + str(i), 'utf-8')).hexdigest()
        i += 1

    object_name = urllib.parse.quote_plus(filename_hash)
    mime_type = request.args.get('file_type')

    expires = int(time.time()+60*60*24)
    amz_headers = "x-amz-acl:public-read"

    string_to_sign = "PUT\n\n%s\n%d\n%s\n/%s/exams/%s" % (mime_type, expires, amz_headers, S3_BUCKET, object_name)

    signature = base64.encodebytes(hmac.new(AWS_SECRET_KEY.encode(), string_to_sign.encode('utf8'), sha1).digest())
    signature = urllib.parse.quote_plus(signature.strip())

    url = 'https://s3-us-west-2.amazonaws.com/%s/exams/%s' % (S3_BUCKET, object_name)

    content = json.dumps({
        'signed_request': '%s?AWSAccessKeyId=%s&Expires=%s&Signature=%s' % (url, AWS_ACCESS_KEY, expires, signature),
        'url': url,
        'file_hash': filename_hash
    })
    return content


@exams_bp.route('/add-exam/<lessonid>', methods=("POST", "GET"))
def add_exam(lessonid):
    """Route to either display the form to upload exams or create a new Exam object

    **NOTE: THIS DOES NOT ACTUALLY UPLOAD THE FILE. THAT IS DONE VIA AJAX**"""
    form = AddExamForm()
    try:
        lesson = Lesson.get(Lesson.id == lessonid)
    except:
        flash('Id not found', 'error')
        return redirect(url_for('auth_bp.profile'))
    if form.validate_on_submit():
        Exam.create(
            average_grade=form.average_grade.data,
            filename=form.file.data.filename,
            s3_filename=form.file_hash.data,
            lesson=lesson.id,
            publisher=g.user.user_id,
            number_of_takers=form.number_of_takers.data,
            year=form.year.data,
            semester=form.semester.data
        )
        g.user.karma_points += KarmaPoints.upload_exam.value
        g.user.save()

        return redirect(url_for(".view", lessonid=lesson.id))

    return render_template("exams/add-exam.html", form=form)


@exams_bp.route('/vote/<examid>/<upvote>')
@login_required
def vote(examid, upvote):
    """Route to vote on an exam"""
    # TODO: Move to POST request
    exam = Exam.get(Exam.id == examid)
    vote = True if upvote == "1" else False
    has_voted = exam.has_voted(g.user)
    if exam.has_upvoted(g.user) and vote:
        flash("Error! You have already upvoted this exam!", 'error')
    elif not exam.has_upvoted(g.user) and not vote:
        flash("Error! You have already downvoted this exam!", 'error')
    else:
        sucess, message = exam.vote(g.user, vote)
        if sucess:
            if not has_voted:
                g.user.karma_points += KarmaPoints.exam_vote.value
                g.user.save()
            flash("Success", 'success')
        else:
            flash(message)
    return redirect(url_for(".view", lessonid=exam.lesson.id))
