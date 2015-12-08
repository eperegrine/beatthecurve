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


class Discussion(Model):
    id = PrimaryKeyField(db_column='ID')
    lecture_id = ForeignKeyField(Lecture, db_column='LECTURE_ID')
    name = CharField(db_column='NAME')

    class Meta:
        database = DATABASE
        db_table = 'TBL_DISCUSSION'
        indexes = (
            # create a unique on from/to/date
            (('lecture_id', 'name'), True),
        )
