from flask_wtf import Form
from wtforms.fields import (
    StringField,
    SelectField,
    PasswordField,
)
from wtforms.validators import (
    Email,
    DataRequired,
    ValidationError,
    EqualTo,
)
from .models import User, School


def edu_email_validator(form, field):
    """Raises a ValidationError if an email does not have the .edu top level domain"""
    if not field.data[-4:] == '.edu':
        raise ValidationError('Email must be a .edu email')


def email_in_use_validator(form, field):
    """Raises a ValidationError if an email is already being used"""
    if User.select().where(User.email == form.data).exists():
        raise ValidationError('Email already in use')


def get_schools():
    """Returns a list of tuples containing all schools' ids and names"""
    return [(str(school.school_id), school.name) for school in School.select()]


class SignUpForm(Form):
    """Form to allow users to sign up"""
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    email = StringField('.edu Email',
                        validators=[DataRequired(),
                                    Email(),
                                    edu_email_validator,
                                    email_in_use_validator])
    school = SelectField('School', choices=[("-1", "Choose a university")] + get_schools())
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password',
                                                                                      message='Passwords must match')])


class LoginForm(Form):
    """Form to allow users to login using their email and password"""
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])


class ChangeEmailForm(Form):
    """Form to allow users to update their email"""
    email = StringField('Email', validators=[DataRequired(),Email(), edu_email_validator, email_in_use_validator])


class ChangePasswordForm(Form):
    """Form to allow users to update their password. It requires them to have access to their origin password."""
    current_password = PasswordField('Old Password', validators=[DataRequired()])
    new_password = PasswordField('New Password', validators=[DataRequired()])
    new_password2 = PasswordField('Confirm New Password', validators=[DataRequired(), EqualTo('new_password',
                                                                                      message='Passwords must match')])


class UpdatePermissions(Form):
    """Form to grant a user a permission"""
    user = SelectField('Users', validators=[DataRequired()])
    permission = SelectField('Permission', validators=[DataRequired()], choices=[("-1", "Choose a permission")])