from flask_wtf import Form
from wtforms.fields import (
    SelectMultipleField,
)


class AttendLessonsForm(Form):
    lessons = SelectMultipleField('Lessons')