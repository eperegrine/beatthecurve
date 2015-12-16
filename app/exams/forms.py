from flask_wtf import Form
from wtforms.fields import (
    DecimalField,
    SelectField,
    FileField
)
from wtforms.validators import (
    DataRequired

)


class AddExamForm(Form):
    file = FileField('File', validators=[DataRequired()])
    average_grade = DecimalField('Average Grade', validators=[DataRequired()])
    lesson = SelectField('Lesson', validators=[DataRequired()])