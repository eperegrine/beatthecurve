from flask import Blueprint, render_template, flash, redirect, url_for, g, request
from flask.ext.login import login_required
from app.lesson.models import Lesson
from app.notes.models import Lecture, Discussion
from .forms import AddQuestionForm
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
    for question in questions:
        reply =  Reply.select().where(Reply.question == question.id).order_by(Reply.datetime).limit(1)
        if question.lecture is None:
            data['Misc'].append({'question': question, 'last_post': reply})
        else:
            data[question.lecture.name].append({'question': question, 'last_post': reply})
    print(data)
    return render_template('qa/qa_listing.html', lesson=lesson, questions=data)


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