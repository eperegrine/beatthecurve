from flask_wtf import Form
from wtforms.fields import (
    SelectField,
    StringField,
    FileField
)
from wtforms.validators import (
    ValidationError,
    DataRequired,
    Optional
)

from .models import Lecture, Discussion


def lecture_name_in_use_validator(form, field):
    if Lecture.select().where(
                    (Lecture.name == form.data) & (Lecture.lesson_id == int(form.lesson.data))
    ).exists():
        raise ValidationError('Name already in use')


def discussion_name_in_use_validator(form, field):
    if Discussion.select().where(
                    (Discussion.name == form.data) & (Discussion.lecture_id == int(form.lecture.data))
    ).exists():
        raise ValidationError('Name already in use')


class AddLectureForm(Form):
    # TODO: Add validators
    lesson = SelectField('Lesson')
    name = StringField('Name')


class AddNoteForm(Form):
    lecture = SelectField('Lecture', validators=[DataRequired()])
    discussion = SelectField('Discussion', validators=[Optional()])
    file = FileField('File', validators=[DataRequired()])


class AddDiscussionForm(Form):
    lecture = SelectField('Lecture', validators=[DataRequired()])
    name = StringField('Name', validators=[DataRequired(), discussion_name_in_use_validator])
