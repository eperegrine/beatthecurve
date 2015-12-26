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
from hashlib import sha1

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
    exams = Exam.select().where(Exam.lesson == lessonid)
    semesters = set()
    for exam in exams:
        semesters.add((exam.year, exam.semester))
    print(semesters)
    return render_template('exams/exam_listing.html', lesson=lesson, exams=exams, semesters=sorted(semesters))


@exams_bp.route('/sign_s3/')
def sign_s3():
    # TODO: Move to environment variables
    AWS_ACCESS_KEY = 'AKIAJPAM7ZQCRQQ5GP3Q'
    AWS_SECRET_KEY = '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'
    S3_BUCKET = 'beatthecurve'

    object_name = urllib.parse.quote_plus(request.args.get('file_name'))
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
    })
    return content


@exams_bp.route('/add-exam', methods=("POST", "GET"))
def add_exam():
    form = AddExamForm()
    form.lesson.choices = [(str(lesson.id), lesson.lesson_name) for lesson in Lesson.select()]

    if form.validate_on_submit():
        Exam.create(
            average_grade=form.average_grade.data,
            filename=form.file.data.filename,
            lesson=form.lesson.data,
            publisher=g.user.user_id,
            number_of_takers=form.number_of_takers.data,
            year=form.year.data,
            semester=form.semester.data
        )
        return redirect(url_for(".view", lessonid=form.lesson.data))

    return render_template("exams/add-exam.html", form=form)


@exams_bp.route('/vote/<examid>/<upvote>')
@login_required
def vote(examid, upvote):
    exam = Exam.get(Exam.id == examid)
    vote = True if upvote == "1" else False
    if exam.has_upvoted(g.user) and vote:
        flash("Error! You have already upvoted this exam!")
    elif not exam.has_upvoted(g.user) and not vote:
        flash("Error! You have already downvoted this exam!")
    else:
        sucess, message = exam.vote(g.user, vote)
        if sucess:
            flash("Success")
        else:
            flash(message)
    return redirect(url_for(".detail", examid=examid))


@exams_bp.route('/detail/<examid>')
@login_required
def detail(examid):
    exam = Exam.get(Exam.id == examid)
    return render_template("exams/detail.html", exam=exam)
