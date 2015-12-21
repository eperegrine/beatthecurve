from flask_wtf import Form
from wtforms.fields import (
    StringField,
    SelectField,
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
