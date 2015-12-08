from peewee import *
from app.lesson.models import Lesson
from app.models import DATABASE


class Lecture(Model):
    id = PrimaryKeyField(db_column='ID')
    lesson_id = ForeignKeyField(Lesson, db_column='LESSON_ID')
    name = CharField(db_column='NAME', unique=True)

    class Meta:
        database = DATABASE
        db_table = 'TBL_LECTURE'
