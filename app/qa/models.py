from peewee import *
from app.auth.models import User
from app.notes.models import Lecture, Discussion, Lesson
from app.models import DATABASE
from datetime import datetime


class Question(Model):
    id = PrimaryKeyField(db_column='ID')
    user = ForeignKeyField(User, db_column='USER')
    number_of_posts = IntegerField(db_column='NUMBER_OF_POSTS', default=0)
    document = CharField(db_column='DOCUMENT')
    name = CharField(db_column='NAME', unique=True)
    content = CharField(db_column='CONTENT')

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
