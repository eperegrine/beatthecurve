from flask import Blueprint, render_template, flash, redirect, url_for, g, request
from flask.ext.login import login_required
from app.lesson.models import Lesson
from app.notes.models import Lecture, Discussion
from .forms import AddQuestionForm, AddReplyForm
from .models import Question, Reply
from collections import OrderedDict

qa_bp = Blueprint('qa_bp', __name__, url_prefix='/qa')


@qa_bp.route('/view/<lessonid>')
@login_required
def view(lessonid):
    # TODO: Validate id
    try:
        lesson = Lesson.get(Lesson.id == lessonid)
    except:
        flash('Id not found')
        return redirect(url_for('auth_bp.profile'))
    data = OrderedDict()
    data['Misc'] = []
    lectures = Lecture.select().where(Lecture.lesson_id == lessonid)
    for lecture in lectures:
        data[lecture.name] = []
    questions = Question.select().where(Question.lesson == lessonid)
    last_posts = {}
    for question in questions:
        reply = Reply.select().where(Reply.question == question.id).order_by(Reply.datetime).limit(1)
        print(reply)
        if question.lecture is None:
            data['Misc'].append({'question': question, 'last_post': reply})
        else:
            data[question.lecture.name].append({'question': question})
        try:
            last_posts[question.name] = [r for r in reply][0]
        except:
            pass

    if len(data['Misc']) < 1:
        del data['Misc']
    return render_template('qa/qa_listing.html', lesson=lesson, questions=data, last_posts=last_posts)


@qa_bp.route('/add-question/<lessonid>', methods=('POST', 'GET'))
@login_required
def add_question(lessonid):
    form = AddQuestionForm()
    form.lecture.choices = [(str(lecture.id), lecture.name) for lecture in
                            Lecture.select().where(Lecture.lesson_id == int(lessonid))]
    form.lecture.choices.append(('-1', "N/A"))
    form.discussion.choices = [('-1', "None")]

    if request.method == 'POST':
        form.discussion.choices += [(str(discussion.id), discussion.name) for discussion in Discussion.select().where(Discussion.lecture_id == form.lecture.data)]

    if form.validate_on_submit():
        print(form.discussion.data)
        if form.lecture.data != '-1' and form.lecture.data != 'None':
            # TODO: Add Error Handling
            if form.discussion.data != '-1' and form.discussion.data != 'None':
                Question.create(user=g.user.user_id, name=form.name.data, content=form.content.data, lecture=form.lecture.data,
                                discussion=form.discussion.data, lesson=lessonid)
            else:
                Question.create(user=g.user.user_id, name=form.name.data, content=form.content.data, lecture=form.lecture.data,
                                lesson=lessonid)
        else:
            Question.create(user=g.user.user_id, name=form.name.data, content=form.content.data, lesson=lessonid)
        return redirect(url_for(".view", lessonid=lessonid))
    return render_template('qa/add_question.html', form=form)


@qa_bp.route('/detail/<lessonid>/<qid>', methods=('POST', 'GET'))
@login_required
def detail(lessonid, qid):
    lesson = Lesson.get(Lesson.id == lessonid)
    try:
        question = Question.get(Question.id == qid)
    except:
        flash('Id not found')
        return redirect(url_for('.view', lessonid=lessonid))

    replies = Reply.select().where(Reply.question == qid)

    form = AddReplyForm()

    return render_template('qa/detail.html', question=question, detail=detail, lesson=lesson, form=form, replies=replies)


@qa_bp.route('/add-reply/<questionid>', methods=('POST', 'GET'))
@login_required
def add_reply(questionid):
    form = AddReplyForm()

    try:
        question = Question.get(Question.id == questionid)
    except:
        flash('Id not found')
        # TODO: Add 404
        return redirect(url_for('auth_bp.profile'))

    if form.validate_on_submit():
        Reply.create(
            question=question.id,
            user=g.user.user_id,
            content=form.content.data
        )
        question.number_of_posts += 1
        question.save()

    return redirect(url_for(".detail", lessonid=question.lesson.id, qid=question.id))