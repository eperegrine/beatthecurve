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

from app.models import Semester
from datetime import datetime


class AddNoteForm(Form):
    """Form to allow a user to upload a note"""
    file = FileField('File', validators=[DataRequired()])
    description = StringField('Description', validators=[DataRequired()])


class AdminAddNoteForm(AddNoteForm):
    """Form to allow a user to upload a note with a specific year and semester"""
    semester = SelectField('Semester', validators=[DataRequired()], choices=[(str(s.value), s.name.title()) for s in Semester])
    year = SelectField('Year', choices=[(str(i), str(i)) for i in range(datetime.now().year - 5, datetime.now().year + 5)])
