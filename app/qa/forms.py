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
    """Raises a ValidationError if the name for a Question is already being used"""
    if Question.select().where(Question.name == field.data).exists():
        raise ValidationError('Name already in use.')


class AddQuestionForm(Form):
    """Form to allow a user to ask a question"""
    document = StringField('subject', validators=[DataRequired()])
    name = StringField('question', validators=[DataRequired(), question_name_in_use])
    content = TextAreaField('details (optional)', validators=[Optional()])


class AddReplyForm(Form):
    """Form to allow a user to reply to a question"""
    content = StringField('Content', validators=[DataRequired()], id='reply-content')