from flask_wtf import Form
from wtforms.fields import (
    StringField,
    SelectField
)
from wtforms.validators import (
    DataRequired
)


class AddStudyGroupForm(Form):
    lesson = SelectField('Lesson', validators=[DataRequired()])
    location = StringField('Location', validators=[DataRequired()])