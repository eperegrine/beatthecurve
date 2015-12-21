from peewee import *
from app.models import DATABASE
from app.auth.models import User
from app.lesson.models import Lesson
from datetime import datetime


class StudyGroup(Model):
    id = PrimaryKeyField(db_column='ID')
    number_of_members = IntegerField(db_column='NUMBER_OF_MEMBERS', default=1)
    productivity = DecimalField(db_column='PRODUCTIVITY', default=0)
    location = TextField(db_column='LOCATION')
    founder = ForeignKeyField(User, db_column='FOUNDER_ID')
    lesson = ForeignKeyField(Lesson, db_column='LESSON_ID')

    class Meta:
        database = DATABASE
        db_table = 'TBL_STUDY_GROUP'

    def get_next_session(self):
        try:
            query = StudyGroupSession.select().where((StudyGroupSession.datetime >= datetime.now()) & (StudyGroupSession.cancelled == False) & (StudyGroupSession.study_group == self.id)).order_by(StudyGroupSession.datetime.asc())
            for q in query:
                return q
        except Exception as e:
            print(e)
            return None

    def get_all_upcoming_sessions(self):
        try:
            query = StudyGroupSession.select().where((StudyGroupSession.datetime >= datetime.now()) & (StudyGroupSession.study_group == self.id)).order_by(StudyGroupSession.datetime.asc())
            return [q for q in query]
        except Exception as e:
            print(e)
            return None

    def add_member(self, user):
        try:
            if self.is_member(user):
                return None

            self.number_of_members += 1
            self.save()

            StudyGroupMembers.create(
                user=user.user_id,
                study_group=self.id
            )
            return True
        except:
            return None

    def remove_member(self, user):
        try:
            self.number_of_members -= 1
            self.save()
            StudyGroupMembers.delete().where((StudyGroupMembers.study_group == self.id) & (StudyGroupMembers.user == user.user_id)).execute()
            return True
        except:
            return False

    def is_member(self, user):
        if StudyGroupMembers.select().where((StudyGroupMembers.user == user.user_id) & (StudyGroupMembers.study_group == self.id)).exists():
                return True
        return False

    def add_comment(self, content, user):
        try:
            StudyGroupComment.create(
                user=user.user_id,
                content=content,
                study_group=self.id
            )
            return True
        except:
            return False

    def get_comments(self):
        comments = StudyGroupComment.select().where(StudyGroupComment.study_group == self.id)
        return [c for c in comments]

class StudyGroupMembers(Model):
    user = ForeignKeyField(User, db_column='USER_ID')
    study_group = ForeignKeyField(StudyGroup, db_column='STUDY_GROUP_ID')

    class Meta:
        database = DATABASE
        db_table = 'TBL_STUDY_GROUP_MEMBER'


class StudyGroupSession(Model):
    id = PrimaryKeyField(db_column='ID')
    study_group = ForeignKeyField(StudyGroup, db_column='STUDY_GROUP_ID')
    cancelled = BooleanField(default=False, db_column='CANCELLED')
    datetime = DateTimeField(db_column='DATETIME')

    class Meta:
        indexes = (
            (('study_group', 'datetime'), True),
        )
        database = DATABASE
        db_table = 'TBL_STUDY_GROUP_SESSION'


class StudyGroupComment(Model):
    id = PrimaryKeyField(db_column='ID')
    user = ForeignKeyField(User, db_column='USER_ID')
    content = CharField(db_column='CONTENT')
    study_group = ForeignKeyField(StudyGroup, db_column='STUDY_GROUP_ID')

    class Meta:
        database = DATABASE
        db_table = 'TBL_STUDY_GROUP_COMMENT'
