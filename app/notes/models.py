from peewee import *
from app.auth.models import User
from app.lesson.models import Lesson
from app.models import DATABASE


class Lecture(Model):
    id = PrimaryKeyField(db_column='ID')
    lesson_id = ForeignKeyField(Lesson, db_column='LESSON_ID')
    name = CharField(db_column='NAME', unique=True)
    number_of_files = IntegerField(db_column='NUMBER_OF_FILES', default=0)

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


class Note(Model):
    id = PrimaryKeyField(db_column='ID')
    votes = IntegerField(db_column='VOTES', default=0)
    filename = CharField(db_column='FILENAME', unique=True)
    uploader = ForeignKeyField(User, db_column='UPLOADER')
    discussion = ForeignKeyField(Discussion, db_column='DISCUSSION', null=True)
    lecture = ForeignKeyField(Lecture, db_column='LECTURE')

    class Meta:
        database = DATABASE
        db_table = 'TBL_NOTE'


class NoteVote(Model):
    id = PrimaryKeyField(db_column='ID')
    user = ForeignKeyField(User, db_column='USER_ID')
    note = ForeignKeyField(Note, db_column='NOTE_ID')

    class Meta:
        database = DATABASE
        db_table = 'TBL_NOTE_VOTE'
