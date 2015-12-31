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

from .models import Lecture, Discussion, Semester
from datetime import datetime


def lecture_name_in_use_validator(form, field):
    if Lecture.select().where(
                    (Lecture.name == field.data) & (Lecture.lesson_id == int(form.lesson.data)) & (Lecture.year == form.year.data)
    ).exists():
        raise ValidationError('Name already in use')


def discussion_name_in_use_validator(form, field):
    if Discussion.select().where(
                    (Discussion.name == form.data) & (Discussion.lecture_id == int(form.lecture.data))
    ).exists():
        raise ValidationError('Name already in use')


class AddLectureForm(Form):
    lesson = SelectField('Lesson', validators=[DataRequired()])
    name = StringField('Name', validators=[DataRequired(), lecture_name_in_use_validator])
    semester = SelectField('Semester', validators=[DataRequired()], choices=[(str(s.value), s.name.title()) for s in Semester])
    year = SelectField('Year', choices=[(str(i), str(i)) for i in range(datetime.now().year, datetime.now().year + 5)])


class AddNoteForm(Form):
    file = FileField('File', validators=[DataRequired()])
    description = StringField('Description', validators=[DataRequired()])


class AddDiscussionForm(Form):
    lecture = SelectField('Lecture', validators=[DataRequired()])
    name = StringField('Name', validators=[DataRequired(), discussion_name_in_use_validator])
