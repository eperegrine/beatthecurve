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
    """Raises a ValidationError if the name for a lesson is already in use"""
    if Lesson.select().where((Lesson.lesson_name == field.data) & (Lesson.school_id == form.school.data)).exists():
        raise ValidationError("Name already in use.")


def lesson_code_in_use_validators(form, field):
    """Raises a ValidationError if the name for a lesson is already in use"""
    if Lesson.select().where((Lesson.code == field.data) & (Lesson.school_id == form.school.data)).exists():
        raise ValidationError("Code already in use.")


class AttendLessonsForm(Form):
    """Form to allow a user to start to attend lessons"""
    lessons = SelectMultipleField('Lessons', validators=[DataRequired()])


class CreateLessonForm(Form):
    """Form to allow a user to create a lesson"""
    school = HiddenField('school')
    code = StringField('code', validators=[DataRequired(), lesson_code_in_use_validators])
    name = StringField('name', validators=[DataRequired(), lesson_name_in_use_validators])
    professor = StringField('professors, separated by commas', validators=[DataRequired()])
