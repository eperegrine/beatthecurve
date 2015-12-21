from flask_wtf import Form
from wtforms.fields import (
    SelectMultipleField,
)
from wtforms.validators import (
    DataRequired
)


class AttendLessonsForm(Form):
    lessons = SelectMultipleField('Lessons', validators=[DataRequired()])