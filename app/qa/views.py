from flask import Blueprint, render_template, flash, redirect, url_for, g, request, jsonify
from flask.ext.login import login_required
from app.lesson.models import Lesson
from .forms import AddQuestionForm, AddReplyForm
from .models import Question, Reply, QuestionVote, ReplyVote
from app.models import Semester
from datetime import datetime
from app.models import KarmaPoints

qa_bp = Blueprint('qa_bp', __name__, url_prefix='/qa')


@qa_bp.route('/view/<lessonid>')
@login_required
def view(lessonid):
    """Route to display the listing of Questions for a lesson"""
    try:
        lesson = Lesson.get(Lesson.id == lessonid)
    except:
        flash('Id not found', 'error')
        return redirect(url_for('auth_bp.profile'))

    questions = Question.select().where(Question.lesson == lessonid).limit(10)
    last_posts = {}
    semesters = set()

    for question in questions:
        semesters.add((question.year, question.semester))

        reply = Reply.select().where(Reply.question == question.id).order_by(Reply.datetime).limit(1)
        try:
            last_posts[question.name] = [r for r in reply][0]
        except:
            pass

    form = AddQuestionForm()

    comment_form = AddReplyForm()

    return render_template('qa/qa_listing.html', lesson=lesson, questions=questions, form=form, last_posts=last_posts,
                           semesters=sorted(semesters), comment_form=comment_form)


@qa_bp.route('/add-question/<lessonid>', methods=('POST', 'GET'))
@login_required
def add_question(lessonid):
    """Route to handle a POST request to create a Question"""
    form = AddQuestionForm()

    if form.validate_on_submit():
        semester = None
        month = datetime.now().month
        if month < 3 or month == 12:
            semester = Semester.winter
        elif month < 6:
            semester = Semester.spring
        elif month < 9:
            semester = Semester.summer
        else:
            semester = Semester.fall

        Question.create(user=g.user.user_id, name=form.name.data, content=form.content.data, lesson=lessonid, document=form.document.data, semester=semester.value, year=datetime.now().year)

        g.user.karma_points += KarmaPoints.post_question.value
        g.user.save()

        return redirect(url_for(".view", lessonid=lessonid))
    return render_template('qa/add_question.html', form=form)


@qa_bp.route('/add-reply/<questionid>', methods=('POST', 'GET'))
@login_required
def add_reply(questionid):
    """Route to handle a POST request to add a reply to a Question"""
    form = AddReplyForm()

    try:
        question = Question.get(Question.id == questionid)
    except:
        flash('Id not found', 'error')
        return redirect(url_for('auth_bp.profile'))

    if form.validate_on_submit():
        Reply.create(
            question=question.id,
            user=g.user.user_id,
            content=form.content.data
        )
        g.user.karma_points += KarmaPoints.reply_to_question.value
        g.user.save()

        question.number_of_posts += 1
        question.save()

    return redirect(url_for(".view", lessonid=question.lesson.id))


@qa_bp.route('/question-vote', methods=['POST'])
@login_required
def question_vote():
    # Get question id
    question_id = request.form['question_id']
    # Validate question id
    try:
        question = Question.get(Question.id == question_id)
    except:
        return jsonify({'success': False, 'message': 'Invalid id for Question: {}'.format(question_id)})


    # Check if user has already voted
    vote, created = QuestionVote.create_or_get(question=question, user=g.user.user_id)
    if not created:
        vote.voted = not vote.voted
        vote.save()

    question.votes += 1
    question.save()

    return jsonify({'success': True, 'number_of_posts': question.votes})


@qa_bp.route('/reply-vote', methods=['POST'])
@login_required
def reply_vote():
    # Get reply id
    reply_id = request.form['reply_id']
    # Validate reply id
    try:
        reply = Reply.get(Reply.id == reply_id)
    except:
        return jsonify({'success': False, 'message': 'Invalid id for Reply: {}'.format(reply_id)})


    # Check if user has already voted
    vote, created = ReplyVote.create_or_get(reply=reply, user=g.user.user_id)
    if not created:
        vote.voted = not vote.voted
        vote.save()

    reply.votes += 1
    reply.save()

    return jsonify({'success': True, 'number_of_posts': reply.votes})


@qa_bp.route('/get-questions', methods=['POST'])
@login_required
def get_questions():
    lesson_id = request.form['lesson_id']
    question_ids = request.form['question_ids'].split(",")
    try:
        question_ids = [int(i) for i in question_ids]
    except:
        return jsonify({'success': False, 'message': 'Invalid question id'})

    questions = Question.select().where(~(Question.id << question_ids) & (Question.lesson == lesson_id))

    questions_data = {}

    for question in questions:
        questions_data[question.id] = {
            'user': question.user.first_name + " " + question.user.last_name,
            'number_of_posts': question.number_of_posts,
            'document': question.document,
            'question': question.name,
            'details': question.content,
            'semester': question.semester,
            'year': question.year,
            'replies': [
                {
                    'user': reply.user.first_name + " " + reply.user.last_name,
                    'content': reply.content,
                    'datetime': reply.datetime
                } for reply in question.replies()
            ]
        }

    return jsonify({'success': True, 'questions': questions_data})


