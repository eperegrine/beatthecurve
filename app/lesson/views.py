from flask import Blueprint, g, render_template, flash, redirect, url_for, jsonify, request
from flask.ext.login import login_required
from .forms import AttendLessonsForm, CreateLessonForm
from .models import Lesson, LessonStudent, Professor
from app.search.models import UserOption, Option
from app.auth.decorators import permission_required
import json

lesson_bp = Blueprint('lesson_bp', __name__, url_prefix='/lessons')


@lesson_bp.route('/add', methods=('POST', 'GET'))
@login_required
def add():
    """Route to either render the AttendLessonsForm to allow users to attend Lessons or process that form"""
    form = AttendLessonsForm()

    # Setup choices for form
    form.lessons.choices = [(str(lesson.id), lesson.code) for lesson in
                            Lesson.get_unattended_lessons(g.user)]

    # If there are no lessons available display that
    if len(form.lessons.choices) == 0:
        form.lessons.choices =[("-1", "No Lessons Available")]

    # Check if form is valid
    if form.validate_on_submit():
        # TODO: Add exception handling
        lesson_ids = [int(id) for id in form.lessons.data]
        LessonStudent.attend(g.user.user_id, lesson_ids)
        flash("Added!", 'success')

        # Redirect user to their profile page if they have already agreed to one of the possible options
        if UserOption.select().where(UserOption.user == g.user.user_id).exists():
            return redirect(url_for('auth_bp.profile'))
        # Else redirect them to show them the page to agree to options
        else:
            return redirect(url_for("qa_bp.view", lessonid=form.lessons.data[0]))

    return render_template('lesson/add.html', form=form)


@lesson_bp.route('/attend-class', methods=['POST'])
@login_required
def attend_class():
    # form = AttendLessonsForm()
    #
    # # Setup choices for form
    # form.lessons.choices = [(str(lesson.id), lesson.lesson_name + " - " + lesson.professor) for lesson in
    #                         Lesson.get_unattended_lessons(g.user)]
    #
    # # If there are no lessons available display that
    # if len(form.lessons.choices) == 0:
    #     form.lessons.choices =[("-1", "No Lessons Available")]
    #
    # # Check if form is valid
    # if form.validate_on_submit():
    #     # TODO: Add exception handling
    #     lesson_ids = [int(id) for id in form.lessons.data]
    #     LessonStudent.attend(g.user.user_id, lesson_ids)
    #
    #     return jsonify({'success': True})
    # return jsonify({'success': False, 'errors': form.errors})
    attended = 'joined[]' in request.form.keys()
    left = 'left[]' in request.form.keys()
    data = request.data
    print(request.form)
    if attended or left:
        if left:
            for lesson_id in request.form.getlist('left[]'):
                try:
                    LessonStudent.get(student_id=g.user.user_id, lesson_id=lesson_id).delete_instance()
                except Exception as e:
                    print(e)
                    return jsonify({'success': False, 'errors': [e]})
        if attended:
            for lesson_id in request.form.getlist('joined[]'):
                try:
                    LessonStudent.attend(g.user.user_id, [lesson_id])
                except Exception as e:
                    print(e)
                    return jsonify({'success': False, 'errors': [e]})


        return jsonify({'success': True})
    else:
        return jsonify({'success': False, 'errors': ['You must have either joined or left']})



@lesson_bp.route('/create', methods=('POST', 'GET'))
@login_required
@permission_required('lesson_admin')
def create():
    """Route to allow user's with the permission lesson_admin to create new lessons"""
    form = CreateLessonForm()
    form.school.data = g.user.school_id

    if form.validate_on_submit():
        lesson = Lesson.create(
            lesson_name=form.name.data,
            school_id=g.user.school_id,
            code=form.code.data
        )

        professors = form.professor.data.split(",")

        for professor in professors:
            name = professor.split(" ")
            Professor.create(
                lesson_id=lesson.id,
                first_name=name[0],
                last_name=name[1]
            )

        Option.create(
            name='Study Tips',
            description='Are you willing to provide study tips?',
            school=g.user.school_id.school_id,
            lesson=lesson.id
        )

        Option.create(
            name='Sell Old Textbooks',
            description='Would you be willing to sell your old textbooks?',
            school=g.user.school_id.school_id,
            lesson=lesson.id
        )
        return redirect(url_for("auth_bp.profile"))

    return render_template('lesson/create.html', form=form)
