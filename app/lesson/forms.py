from flask_wtf import Form
from wtforms.fields import (
    SelectMultipleField,
    StringField,
    HiddenField
)
from wtforms.validators import (
    DataRequired,
    ValidationError
)

from .models import Lesson


def lesson_name_in_use_validators(form, field):
    if Lesson.select().where((Lesson.lesson_name == field.data) & (Lesson.school_id == form.school.data)).exists():
        raise ValidationError("Name already in use.")


class AttendLessonsForm(Form):
    lessons = SelectMultipleField('Lessons', validators=[DataRequired()])


class CreateLessonForm(Form):
    school = HiddenField('School')
    name = StringField('Name', validators=[DataRequired(), lesson_name_in_use_validators])
    professor = StringField('Professor', validators=[DataRequired()])
