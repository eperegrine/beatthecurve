from flask import Blueprint, render_template, flash, redirect, url_for, request, g, jsonify
from flask.ext.bcrypt import check_password_hash
from flask.ext.login import login_user, login_required, logout_user
from peewee import DoesNotExist
from .forms import SignUpForm, LoginForm, ChangeEmailForm, ChangePasswordForm, UpdatePermissions
from .models import User, UserPermission, Permission
from .decorators import either_permission_required, permission_required
from app.lesson.models import Lesson

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
            flash('Successfully created an account!', 'success')
            login_user(user)
            return redirect(url_for('lesson_bp.add'))
        except Exception as e:
            flash(e, 'error')

    return render_template('auth/signup.html', form=form)


@auth_bp.route('/login', methods=('POST', 'GET'))
def login():
    form = LoginForm()

    if form.validate_on_submit():
        try:
            user = User.get(User.email == form.email.data)
        except DoesNotExist:
            flash('Your email or password does not exist.', 'error')
        else:
            if check_password_hash(user.password, form.password.data):
                login_user(user)
                flash('You have been logged in.', 'success')
                return redirect(url_for('auth_bp.profile'))
            else:
                flash('Your email or password does not exist.', 'error')
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
            flash('Email Updated!', 'success')
            return redirect(url_for('.profile'))

    elif 'change_password' in request.form:
        if change_password_form.validate_on_submit():
            if check_password_hash(g.user.password, change_password_form.current_password.data):
                try:
                    g.user.update_password(change_password_form.new_password.data)
                    flash('Updated Password!', 'success')
                    return redirect(url_for('.profile'))
                # TODO: improve error handling
                except:
                    flash('There was an error!', 'error')
        else:
            flash('Incorrect Password', 'error')

    return render_template('auth/profile.html', change_email_form=change_email_form,
                           change_password_form=change_password_form)


@auth_bp.route('/admin/<lessonid>')
@login_required
@either_permission_required(['lecture_admin', 'discussion_admin'])
def admin(lessonid):
    try:
        lesson = Lesson.get(Lesson.id == lessonid)
    except:
        flash('Id not found', 'error')
        return redirect(url_for('auth_bp.profile'))
    return render_template('auth/admin.html',lesson=lesson)


@auth_bp.route('/modify-permissions', methods=('POST', 'GET'))
@login_required
@permission_required('super_user')
def modify_permissions():
    # Get all users in school
    users = User.select().where(User.school_id == g.user.school_id)

    form = UpdatePermissions()
    form.user.choices = [(str(u.user_id), u.first_name + " " + u.last_name) for u in users]

    if form.permission.data != "None":
        permissions = Permission.select().where(Permission.school == g.user.school_id)
        form.permission.choices = [(str(p.id), p.name) for p in permissions]

    if form.validate_on_submit():
        user_permission, created = UserPermission.create_or_get(permission=form.permission.data, user=form.user.data)
        if not created:
            user_permission.delete_instance()
        return redirect(url_for(".profile"))

    return render_template('auth/modify_permissions.html', users=users, form=form)


@auth_bp.route('/get-permissions/<userid>')
@login_required
@permission_required('super_user')
def get_permissions(userid):
    try:
        user_permissions = [p.permission.id for p in UserPermission.select().where(UserPermission.user == userid)]
        print(user_permissions)
        permissions = Permission.select().where(Permission.school == g.user.school_id)
        print([p.id for p in permissions])
        return jsonify(
            {'data': [
                {
                    'id': str(p.id),
                    'name': p.name,
                    'has': p.id in user_permissions
                } for p in permissions
            ]})
    except Exception as e:
        return jsonify({'error': e})

