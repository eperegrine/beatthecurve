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
    """Form to create a StudyGroup"""
    lesson = SelectField('Lesson', validators=[DataRequired()])
    location = StringField('Location', validators=[DataRequired()])


class AddStudyGroupSessionForm(Form):
    """Form to create a StudyGroupSession(s) for a StudyGroup.

    Provides the option to automatically generate StudyGroupSessions until a given date
    """
    date = DateField('Date', validators=[DataRequired()], format='%d %B, %Y')
    time = TimeField('Time', validators=[DataRequired()])
    repeat = BooleanField('Repeat', validators=[Optional()])
    repeat_frequency = SelectField('Repeat Every', validators=[Optional()], choices=[
        (str(i), str(i) + ' days') for i in range(1, 15)
    ])
    repeat_until = DateField('Repeat Until', validators=[Optional()], format='%d %B, %Y')


class AddComment(Form):
    """Form to allow users to comment on a studygroup"""
    comment = StringField('Comment', validators=[DataRequired()])


class ContactOrganiserForm(Form):
    """Form to send an email to the organiser of a StudyGroup"""
    message = TextAreaField('Message', validators=[DataRequired()])
    study_group = HiddenField()