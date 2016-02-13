from flask_wtf import Form


class UserOptionsForm(Form):
    """Form to allow users to agree or disagree with options

    It is autopopulated in the controller/view - views.py - as each option
    is a select field therefore depends on a User's school.

    """
    pass