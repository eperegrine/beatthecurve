from flask_wtf import Form
from wtforms.fields import (
    SelectField,
    StringField,
    FileField
)
from wtforms.validators import (
    ValidationError,
    DataRequired
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


class AddNoteForm(Form):
    lecture = SelectField('Lecture', validators=[DataRequired()])
    discussion = SelectField('Discussion')
    file = FileField('File', validators=[DataRequired()])
