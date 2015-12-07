from flask import Blueprint, render_template, flash, redirect, url_for
from flask.ext.bcrypt import check_password_hash
from flask.ext.login import login_user, login_required, logout_user
from peewee import DoesNotExist
from .forms import SignUpForm, LoginForm
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


@auth_bp.route('/login', methods=('POST', 'GET'))
def login():
    form = LoginForm()

    if form.validate_on_submit():
        try:
            user = User.get(User.email == form.email.data)
        except DoesNotExist:
            flash('Your email or password does not exist.')
        else:
            if check_password_hash(user.password, form.password.data):
                login_user(user)
                flash('You have been logged in.')
                return redirect(url_for('.login'))
            else:
                flash('Your email or password does not exist.')
    return render_template('auth/login.html', form=form)


@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for(".login"))


@auth_bp.route('/profile')
@login_required
def profile():
    return render_template('auth/profile.html')