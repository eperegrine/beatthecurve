from flask_wtf import Form
from wtforms.fields import (
    StringField,
    SelectField,
    DateTimeField
)
from wtforms.validators import (
    DataRequired
)


class AddStudyGroupForm(Form):
    lesson = SelectField('Lesson', validators=[DataRequired()])
    location = StringField('Location', validators=[DataRequired()])


class AddStudyGroupSession(Form):
    datetime = DateTimeField('Datetime', validators=[DataRequired()])
