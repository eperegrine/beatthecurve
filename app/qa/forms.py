from flask_wtf import Form

from wtforms.fields import (
    SelectField,
    StringField,
    TextAreaField
)

from wtforms.validators import (
    Optional,
    DataRequired,
    ValidationError
)

from .models import Question


def question_name_in_use(form, field):
    if Question.select().where(field.data).exists():
        raise ValidationError('Name already in use.')


class AddQuestionForm(Form):
    lesson = SelectField('Lesson', validators=[Optional()])
    lecture = SelectField('Lecture', validators=[Optional()])
    discussion = SelectField('Discussion', validators=[Optional()])
    name = StringField('Name', validators=[DataRequired(), question_name_in_use])
    content = TextAreaField('Content', validators=[DataRequired()])
