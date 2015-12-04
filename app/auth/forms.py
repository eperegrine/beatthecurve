from flask_wtf import Form
from wtforms.fields import (
    StringField,
    SelectField,
    PasswordField,
    SubmitField,
)
from wtforms.validators import (
    Email,
    DataRequired,
    ValidationError,
    Length,
    EqualTo,
)
from .models import User, School


def edu_email_validator(form, field):
    if field.data[-4:] is not '.edu':
        raise ValidationError('Email must be a .edu email')


def email_in_use_validator(form, field):
    if User.select().where(User.email == form.data).exists():
        raise ValidationError('Email already in use')


class SignUpForm(Form):
    email = StringField('Email',
                        validators=[DataRequired(),
                                    Email(),
                                    edu_email_validator,
                                    email_in_use_validator])
    school = SelectField('School', validators=[DataRequired()], choices=[school.name for school in School.select()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=5)])
    password2 = PasswordField('Password Again', validators=[DataRequired(), EqualTo(password)])
    submit = SubmitField('Sign Up')


class LoginForm(Form):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    login = SubmitField('Login')
