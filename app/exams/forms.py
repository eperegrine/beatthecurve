from flask_wtf import Form
from wtforms.fields import (
    DecimalField,
    SelectField,
    FileField,
    IntegerField,
    HiddenField,
    StringField,
    TextAreaField
)
from wtforms.validators import (
    DataRequired,
    Optional,
)

from datetime import datetime
from app.models import Semester


class AddExamForm(Form):
    """Form to allow users to upload an exam"""
    file_hash = HiddenField()
    file = FileField('file', validators=[DataRequired()])
    filename = StringField('filename', validators=[DataRequired()])
    description = StringField('description', validators=[Optional()])
    # average_grade = DecimalField('average grade', validators=[DataRequired()])
    # number_of_takers = IntegerField('number of takers', validators=[DataRequired()])
    # semester = SelectField('semester', validators=[DataRequired()], choices=[(str(s.value), s.name.title()) for s in Semester])
    # year = SelectField('year', choices=[(str(i), str(i)) for i in range(datetime.now().year, datetime.now().year + 5)])
