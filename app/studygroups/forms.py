from flask_wtf import Form
from wtforms.fields import (
    StringField,
    SelectField,
    TextAreaField,
    HiddenField,
    BooleanField
)
from wtforms.validators import (
    DataRequired,
    Optional
)

from wtforms_components import TimeField, DateField


class AddStudyGroupForm(Form):
    lesson = SelectField('Lesson', validators=[DataRequired()])
    location = StringField('Location', validators=[DataRequired()])


class AddStudyGroupSessionForm(Form):
    date = DateField('Date', validators=[DataRequired()], format='%d %B, %Y')
    time = TimeField('Time', validators=[DataRequired()])
    repeat = BooleanField('Repeat', validators=[Optional()])
    repeat_frequency = SelectField('Repeat Every', validators=[Optional()], choices=[
        (str(i), str(i) + ' days') for i in range(1, 15)
    ])
    repeat_until = DateField('Repeat Until', validators=[Optional()], format='%d %B, %Y')


class AddComment(Form):
    comment = StringField('Comment', validators=[DataRequired()])


class ContactOrganiserForm(Form):
    message = TextAreaField('Message', validators=[DataRequired()])
    study_group = HiddenField()