from flask import Blueprint, g, render_template, redirect, url_for, flash, jsonify
from flask.ext.login import login_required
from .forms import UserOptionsForm
from .models import Option, UserOption
from wtforms.fields import BooleanField
from app.lesson.models import Lesson
from app.auth.models import User
from app.lesson.models import LessonStudent

search_bp = Blueprint('search_bp', __name__, url_prefix='/search')


@search_bp.route('/options', methods=('POST', 'GET'))
@login_required
def options():
    for option in Option.select().where(Option.school == g.user.school_id):
        user_option = UserOption.get_or_create(option=option.id, user=g.user.user_id)[0]
        print(user_option.agreed)
        setattr(UserOptionsForm, option.name, BooleanField(option.description, default=user_option.agreed))

    form = UserOptionsForm()

    if form.validate_on_submit():
        for key, value in form.data.items():
            option = Option.get(Option.name == key)
            user_option = UserOption.get(option=option.id, user=g.user.user_id)
            user_option.agreed = value
            user_option.save()
        return redirect(url_for("auth_bp.profile"))

    return render_template('search/options.html', form=form)


@search_bp.route('/view/<lessonid>')
@login_required
def view(lessonid):
    try:
        lesson = Lesson.get(Lesson.id == lessonid)
    except:
        flash('Id not found')
        return redirect(url_for('auth_bp.profile'))

    # Get all users in lesson
    users = [ls.student_id.user_id for ls in LessonStudent.select().where(LessonStudent.lesson_id == lesson.id)]
    options = {}
    for option in Option.select().where(Option.school == g.user.school_id):
        options[option.id] = option.name
    # Get all matching lessons
    data = []
    for user_id in users:
        user_options = UserOption.select().where((UserOption.user == user_id) & (UserOption.agreed == True))
        user_options_list = [options[uo.option.id] for uo in user_options]
        if len(user_options_list) < 1:
            continue
        user = User.get(User.user_id == user_id)
        data.append({'name': user.first_name + " " + user.last_name, 'email': user.email, 'options': user_options_list})
    return render_template('search/listing.html', lesson=lesson, users=data)