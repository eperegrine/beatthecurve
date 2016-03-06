from peewee import *
from app.auth.models import User
from app.notes.models import Lesson
from app.models import DATABASE, Semester
from datetime import datetime


class Question(Model):
    """Model representing a Question asked by a user"""
    id = PrimaryKeyField(db_column='ID')
    user = ForeignKeyField(User, db_column='USER')
    number_of_posts = IntegerField(db_column='NUMBER_OF_POSTS', default=0)
    document = CharField(db_column='DOCUMENT')
    name = CharField(db_column='NAME', unique=True)
    content = CharField(db_column='CONTENT')
    semester = IntegerField(db_column='SEMESTER')
    year = IntegerField(db_column='YEAR', default=2016)
    lesson = ForeignKeyField(Lesson, db_column='LESSON_ID')

    class Meta:
        database = DATABASE
        db_table = 'TBL_QUESTION'

    def replies(self):
        """Method to return all the replies for the instance of a Question"""
        try:
            return Reply.select().where(Reply.question == self.id)
        except Exception as e:
            print(e)
            return []


class Reply(Model):
    """Model representing a reply to a question"""
    id = PrimaryKeyField(db_column='ID')
    question = ForeignKeyField(Question, db_column='QUESTION')
    user = ForeignKeyField(User, db_column='USER')
    content = CharField(db_column='CONTENT')
    datetime = DateTimeField(db_column='DATETIME', default=datetime.now)

    class Meta:
        database = DATABASE
        db_table = 'TBL_REPLY'


class QuestionVote(Model):
    """Model representing a vote on a question"""
    id = PrimaryKeyField(db_column='ID')
    question = ForeignKeyField(Question, db_column='QUESTION_ID')
    user = ForeignKeyField(User, db_column='USER_ID')
    voted = BooleanField(default=True, db_column='VOTED')

    class Meta:
        database = DATABASE
        db_table = 'TBL_QUESTION_VOTE'
        indexes = (
            (('user', 'question'), True),
        )


class ReplyVote(Model):
    """Model representing a vote on a reply"""
    id = PrimaryKeyField(db_column='ID')
    reply = ForeignKeyField(Reply, db_column='REPLY_ID')
    user = ForeignKeyField(User, db_column='USER_ID')
    voted = BooleanField(default=True, db_column='VOTED')

    class Meta:
        database = DATABASE
        db_table = 'TBL_REPLY_VOTE'
        indexes = (
            (('user', 'reply'), True),
        )

