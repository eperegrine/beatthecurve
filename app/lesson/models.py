from peewee import *
from app.models import DATABASE
from app.auth.models import School, User


class Lesson(Model):
    id = PrimaryKeyField(db_column='ID')
    lesson_name = CharField(db_column='NAME', unique=True)
    professor = CharField(db_column='PROFESSOR')
    school_id = ForeignKeyField(School, db_column='SCHOOL')

    class Meta:
        database = DATABASE
        db_table = 'TBL_LESSON'


class LessonStudent(Model):
    student_id = ForeignKeyField(User, db_column='STUDENT_ID')
    lesson_id = ForeignKeyField(Lesson, db_column='LESSON_ID')

    class Meta:
        database = DATABASE
        db_table = 'TBL_LESSON_STUDENT'
        primary_key = CompositeKey('student_id', 'lesson_id')
