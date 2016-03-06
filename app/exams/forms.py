from flask_wtf import Form
from wtforms.fields import (
    DecimalField,
    SelectField,
    FileField,
    IntegerField,
    HiddenField,
    StringField
)
from wtforms.validators import (
    DataRequired

)

from datetime import datetime
from app.models import Semester


class AddExamForm(Form):
    """Form to allow users to upload an exam"""
    file_hash = HiddenField()
    file = FileField('File', validators=[DataRequired()])
    filename = StringField('Filename', validators=[DataRequired()])
    average_grade = DecimalField('Average Grade', validators=[DataRequired()])
    number_of_takers = IntegerField('Number Of Takers', validators=[DataRequired()])
    semester = SelectField('Semester', validators=[DataRequired()], choices=[(str(s.value), s.name.title()) for s in Semester])
    year = SelectField('Year', choices=[(str(i), str(i)) for i in range(datetime.now().year, datetime.now().year + 5)])
