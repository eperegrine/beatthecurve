from peewee import *
from app.notes.models import Lesson
from app.auth.models import User
from app.models import DATABASE


class Exam(Model):
    id = PrimaryKeyField(db_column='ID')
    average_grade = DecimalField(db_column='AVERAGE_GRADE')
    filename = CharField(unique=True, db_column='FILENAME')
    lesson = ForeignKeyField(Lesson, db_column='LESSON')
    number_of_takers = IntegerField(default=0, db_column='NUMBER_OF_TAKERS')
    publisher = ForeignKeyField(User, db_column='PUBLISHER')

    class Meta:
        database = DATABASE
        db_table = 'TBL_EXAM'


class ExamVote(Model):
    id = PrimaryKeyField(db_column='ID')
    user = ForeignKeyField(User, db_column='USER_ID')
    exam = ForeignKeyField(Exam, db_column='EXAM_ID')
    upvote = BooleanField(db_column='UPVOTE')

    class Meta:
        database = DATABASE
        db_table = 'TBL_EXAM_VOTE'
