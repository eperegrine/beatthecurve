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

    @classmethod
    def get_unattended_lessons(cls, user_id, school_id):
        schools_lessons = cls.select().where(cls.school_id == school_id)
        users_lessons = LessonStudent.select().where(LessonStudent.student_id == user_id)
        lessons = []
        for lesson in schools_lessons:
            if lesson not in users_lessons:
                lessons.append(lesson)
        return lessons


class LessonStudent(Model):
    student_id = ForeignKeyField(User, db_column='STUDENT_ID')
    lesson_id = ForeignKeyField(Lesson, db_column='LESSON_ID')

    class Meta:
        database = DATABASE
        db_table = 'TBL_LESSON_STUDENT'
        primary_key = CompositeKey('student_id', 'lesson_id')

    @classmethod
    def get_attended_lessons(cls, user_id):
        users_lessons = cls.select().where(LessonStudent.student_id == user_id)
        lessons = [Lesson.get(Lesson.id == lesson.lesson_id) for lesson in users_lessons]
        return lessons

    @classmethod
    def attend(cls, user_id, lesson_ids):
        # TODO: Validate user_id and lesson_ids so they are in the same school
        for lesson_id in lesson_ids:
            LessonStudent.create(student_id=user_id, lesson_id=lesson_id)