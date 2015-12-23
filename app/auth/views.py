from flask import Blueprint, render_template, flash, redirect, url_for, request, g
from flask.ext.bcrypt import check_password_hash
from flask.ext.login import login_user, login_required, logout_user
from peewee import DoesNotExist
from .forms import SignUpForm, LoginForm, ChangeEmailForm, ChangePasswordForm
from .models import User

auth_bp = Blueprint('auth_bp', __name__)


@auth_bp.route('/signup', methods=('POST', 'GET'))
def signup():
    form = SignUpForm()

    if form.validate_on_submit():
        try:
            user = User.create_user(
                email=form.email.data,
                password=form.password.data,
                school_id=int(form.school.data),
                first_name=form.first_name.data,
                last_name=form.last_name.data
            )
            flash('Successfully created an account!')
            login_user(user)
            return redirect(url_for('lesson_bp.add'))
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


@auth_bp.route('/profile', methods=('POST', 'GET'))
@login_required
def profile():
    change_email_form = ChangeEmailForm()
    change_password_form = ChangePasswordForm()

    if 'change_email' in request.form:
        if change_email_form.validate_on_submit():
            # TODO: Add Error handling
            g.user.email = change_email_form.email.data
            g.user.save()
            flash('Email Updated!')
            return redirect(url_for('.profile'))

    elif 'change_password' in request.form:
        if change_password_form.validate_on_submit():
            if check_password_hash(g.user.password, change_password_form.current_password.data):
                try:
                    g.user.update_password(change_password_form.new_password.data)
                    flash('Updated Password!')
                    return redirect(url_for('.profile'))
                # TODO: improve error handling
                except:
                    flash('There was an error!')
        else:
            flash('Incorrect Password')

    return render_template('auth/profile.html', change_email_form=change_email_form,
                           change_password_form=change_password_form)