from peewee import *
from app.auth.models import User
from app.notes.models import Lecture, Discussion, Lesson
from app.models import DATABASE, Semester
from datetime import datetime


class Question(Model):
    id = PrimaryKeyField(db_column='ID')
    user = ForeignKeyField(User, db_column='USER')
    number_of_posts = IntegerField(db_column='NUMBER_OF_POSTS', default=0)
    document = CharField(db_column='DOCUMENT')
    name = CharField(db_column='NAME', unique=True)
    content = CharField(db_column='CONTENT')
    semester = IntegerField(db_column='SEMESTER', default=Semester.winter.value)
    year = IntegerField(db_column='YEAR', default=2016)
    class Meta:
        database = DATABASE
        db_table = 'TBL_QUESTION'


class Reply(Model):
    id = PrimaryKeyField(db_column='ID')
    question = ForeignKeyField(Question, db_column='QUESTION')
    user = ForeignKeyField(User, db_column='USER')
    content = CharField(db_column='CONTENT')
    datetime = DateTimeField(db_column='DATETIME', default=datetime.now)

    class Meta:
        database = DATABASE
        db_table = 'TBL_REPLY'
