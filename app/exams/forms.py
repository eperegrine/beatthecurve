from flask_wtf import Form
from wtforms.fields import (
    DecimalField,
    SelectField,
    FileField,
    IntegerField
)
from wtforms.validators import (
    DataRequired

)

from datetime import datetime
from app.models import Semester


class AddExamForm(Form):
    file = FileField('File', validators=[DataRequired()])
    average_grade = DecimalField('Average Grade', validators=[DataRequired()])
    lesson = SelectField('Lesson', validators=[DataRequired()])
    number_of_takers = IntegerField('Number Of Takers', validators=[DataRequired()])
    semester = SelectField('Semester', validators=[DataRequired()], choices=[(str(s.value), s.name.title()) for s in Semester])
    year = SelectField('Year', choices=[(str(i), str(i)) for i in range(datetime.now().year, datetime.now().year + 5)])
