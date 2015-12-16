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


class AddExamForm(Form):
    file = FileField('File', validators=[DataRequired()])
    average_grade = DecimalField('Average Grade', validators=[DataRequired()])
    lesson = SelectField('Lesson', validators=[DataRequired()])
    number_of_takers = IntegerField('Number Of Takers', validators=[DataRequired()])