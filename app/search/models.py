from app.models import DATABASE
from peewee import *
from app.auth.models import User, School
from app.lesson.models import Lesson


class Option(Model):
    """Model representing an option a user can subscribe to"""
    id = PrimaryKeyField(db_column='ID')
    name = CharField(db_column='NAME')
    description = CharField(db_column='DESCRIPTION')
    lesson = ForeignKeyField(Lesson, db_column='LESSON_ID')

    class Meta:
        database = DATABASE
        db_table = "TBL_OPTION"
        indexes = (
            (('name', 'school'), True),
        )


class UserOption(Model):
    """Model representing a user agreeing or disagreeing to an option"""
    id = PrimaryKeyField(db_column='ID')
    user = ForeignKeyField(User, db_column='USER_ID')
    option = ForeignKeyField(Option, db_column='OPTION_ID')
    agreed = BooleanField(db_column='AGREED', default=False)

    class Meta:
        database = DATABASE
        db_table = "TBL_USER_OPTION"
