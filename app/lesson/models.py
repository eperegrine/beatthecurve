from peewee import *
from app.models import DATABASE, Semester
from app.auth.models import School, User
from datetime import datetime


class Lesson(Model):
    """Model representing a lesson a user can attend.

    They are specific to a school and must have unique names
    within a school.
    """
    id = PrimaryKeyField(db_column='ID')
    lesson_name = CharField(db_column='NAME')
    professor = CharField(db_column='PROFESSOR')
    school_id = ForeignKeyField(School, db_column='SCHOOL')

    class Meta:
        database = DATABASE
        db_table = 'TBL_LESSON'
        indexes = (
            (('NAME', 'SCHOOL'), True),
        )

    @classmethod
    def get_unattended_lessons(cls, user):
        """Class method to get the lessons a user is not currently enrolled in

        `user` is an instance of `app.auth.models.User`
        """
        schools_lessons = cls.select().where(cls.school_id == user.school_id)
        users_lessons = [ls.lesson_id.id for ls in LessonStudent.select().where(LessonStudent.student_id == user.user_id)]
        lessons = []
        for lesson in schools_lessons:
            if lesson.id not in users_lessons:
                lessons.append(lesson)
        return lessons


class LessonStudent(Model):
    """Model representing a user attending a lesson in a specific year and semester"""
    student_id = ForeignKeyField(User, db_column='STUDENT_ID')
    lesson_id = ForeignKeyField(Lesson, db_column='LESSON_ID')
    semester = IntegerField(db_column='SEMESTER')
    year = IntegerField(db_column='YEAR')

    class Meta:
        database = DATABASE
        db_table = 'TBL_LESSON_STUDENT'
        #primary_key = CompositeKey('student_id', 'lesson_id')
        # TODO: Add composite key

    @classmethod
    def get_attended_lessons(cls, user_id):
        """Class method to get all the Lessons a user is currently attending"""
        users_lessons = cls.select().where(LessonStudent.student_id == user_id)
        lessons = [Lesson.get(Lesson.id == lesson.lesson_id) for lesson in users_lessons]
        return lessons

    @classmethod
    def attend(cls, user_id, lesson_ids):
        """Class method to create LessonStudent objects for every lesson a user wants to attend"""
        # TODO: Validate user_id and lesson_ids so they are in the same school
        # TODO: Update semesters
        for lesson_id in lesson_ids:
            month = datetime.now().month
            if month < 3 or month == 12:
                semester = Semester.winter
            elif month < 6:
                semester = Semester.spring
            elif month < 9:
                semester = Semester.summer
            else:
                semester = Semester.fall
            LessonStudent.create(student_id=user_id, lesson_id=lesson_id, semester=semester.value,
                                 year=datetime.now().year)