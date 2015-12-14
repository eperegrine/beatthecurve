from peewee import *
from app.auth.models import User
from app.notes.models import Lecture, Discussion, Lesson
from app.models import DATABASE


class Question(Model):
    id = PrimaryKeyField(db_column='ID')
    user = ForeignKeyField(User, db_column='USER')
    number_of_posts = IntegerField(db_column='NUMBER_OF_POSTS', default=0)
    # TODO: Add Exam Foreign Key
    lecture = ForeignKeyField(Lecture, db_column='LECTURE', null=True)
    lesson = ForeignKeyField(Lesson, db_column='LESSON', null=True)
    discussion = ForeignKeyField(Discussion, db_column='DISCUSSION', null=True)
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

    class Meta:
        database = DATABASE
        db_table = 'TBL_REPLY'
