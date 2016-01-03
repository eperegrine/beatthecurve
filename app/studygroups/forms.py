from flask_wtf import Form
from wtforms.fields import (
    StringField,
    SelectField,
    TextAreaField,
    HiddenField
)
from wtforms.validators import (
    DataRequired
)

from wtforms_components import TimeField, DateField


class AddStudyGroupForm(Form):
    lesson = SelectField('Lesson', validators=[DataRequired()])
    location = StringField('Location', validators=[DataRequired()])


class AddStudyGroupSessionForm(Form):
    date = DateField('Date', validators=[DataRequired()])
    time = TimeField('Time', validators=[DataRequired()])


class AddComment(Form):
    comment = StringField('Comment', validators=[DataRequired()])


class ContactOrganiserForm(Form):
    message = TextAreaField('Message', validators=[DataRequired()])
    study_group = HiddenField()