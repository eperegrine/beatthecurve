from flask_wtf import Form
from wtforms.fields import (
    SelectField,
    StringField,
)
from wtforms.validators import (
    ValidationError,
)

from .models import Lecture


def lecture_name_in_use_validator(form, field):
    if Lecture.select().where(
                    (Lecture.name == form.data) & (Lecture.lesson_id == int(form.lesson.data))
    ).exists():
        raise ValidationError('Name already in use')


class AddLectureForm(Form):
    lesson = SelectField('Lesson')
    name = StringField('Name')
