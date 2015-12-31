from peewee import *
from app.auth.models import User
from app.lesson.models import Lesson
from app.models import DATABASE
from enum import Enum


class Semester(Enum):
    winter = 1
    fall = 2
    spring = 3
    summer = 4


class Lecture(Model):
    id = PrimaryKeyField(db_column='ID')
    lesson_id = ForeignKeyField(Lesson, db_column='LESSON_ID')
    name = CharField(db_column='NAME')
    number_of_files = IntegerField(db_column='NUMBER_OF_FILES', default=0)
    semester = IntegerField(db_column='SEMESTER', default=Semester.winter.value)
    year = IntegerField(db_column='YEAR', default=2015)

    class Meta:
        database = DATABASE
        db_table = 'TBL_LECTURE'
        indexes = (
            (('NAME', 'YEAR', 'LESSON_ID'), True)
        )


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

    class Meta:
        database = DATABASE
        db_table = 'TBL_NOTE'

    def has_voted(self, user):
        if NoteVote.select().where((NoteVote.user == user.user_id) & (NoteVote.note == self.id)).exists():
            return True
        return False

    def has_upvoted(self, user):
        if NoteVote.select().where((NoteVote.user == user.user_id) & (NoteVote.note == self.id) & (NoteVote.upvote == True)).exists():
            return True
        return False

    def vote(self, user, upvote):
        if not self.has_voted(user):
            try:
                NoteVote.create(
                    user=user.user_id,
                    note=self.id,
                    upvote=upvote,
                )
            except Exception as e:
                return False, str(e)
        else:
            try:
                nv = NoteVote.get(NoteVote.user == user.user_id, NoteVote.note == self.id)
                nv.upvote = upvote
                nv.save()
            except Exception as e:
                return False, str(e)
        if upvote:
            self.votes += 1
        else:
            self.votes -= 1
        self.save()
        return True, ""


class NoteVote(Model):
    id = PrimaryKeyField(db_column='ID')
    user = ForeignKeyField(User, db_column='USER_ID')
    note = ForeignKeyField(Note, db_column='NOTE_ID')
    upvote = BooleanField(db_column='UPVOTE')

    class Meta:
        database = DATABASE
        db_table = 'TBL_NOTE_VOTE'
