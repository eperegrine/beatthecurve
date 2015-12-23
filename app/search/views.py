from flask import Blueprint, g, render_template, redirect, url_for
from flask.ext.login import login_required
from .forms import UserOptionsForm
from .models import Option, UserOption
from wtforms.fields import BooleanField

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

