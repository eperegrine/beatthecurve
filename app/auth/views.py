from flask import Blueprint, render_template, flash, redirect, url_for
from .forms import SignUpForm
from .models import User

auth_bp = Blueprint('auth_bp', __name__)


@auth_bp.route('/signup', methods=('POST', 'GET'))
def signup():
    form = SignUpForm()

    if form.validate_on_submit():
        try:
            User.create_user(
                email=form.email.data,
                password=form.password.data,
                school_id=int(form.school.data)
            )
            flash('Successfully created an account!')
            return redirect(url_for('.signup'))
        except Exception as e:
            flash(e)

    return render_template('auth/signup.html', form=form)
