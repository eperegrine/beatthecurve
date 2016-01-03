from peewee import *
from app.models import DATABASE
from app.auth.models import User
from app.lesson.models import Lesson
from datetime import datetime


class Message(Model):
    id = PrimaryKeyField(db_column='ID')
    text = CharField(db_column='TEXT')
    sender = ForeignKeyField(User, db_column='USER_ID')
    lesson = ForeignKeyField(Lesson, db_column='LESSON_ID')
    sent = DateTimeField(default=datetime.now, db_column='DATETIME')

    class Meta:
        database = DATABASE
        db_table = 'TBL_MESSAGE'
