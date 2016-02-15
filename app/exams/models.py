from peewee import *
from app.notes.models import Lesson
from app.auth.models import User
from app.models import DATABASE, Semester


class Exam(Model):
    """Model to represent an exam

    An exam has a unique id and filename.
    """
    id = PrimaryKeyField(db_column='ID')
    average_grade = DecimalField(db_column='AVERAGE_GRADE')
    filename = CharField(db_column='FILENAME')
    s3_filename = CharField(db_column='S3_FILENAME')
    lesson = ForeignKeyField(Lesson, db_column='LESSON')
    number_of_takers = IntegerField(default=0, db_column='NUMBER_OF_TAKERS')
    publisher = ForeignKeyField(User, db_column='PUBLISHER')
    votes = IntegerField(db_column='VOTES', default=0)
    year = IntegerField(db_column='YEAR', default=2015)
    semester = IntegerField(db_column='SEMESTER', default=Semester.winter.value)

    class Meta:
        database = DATABASE
        db_table = 'TBL_EXAM'
        
    def has_voted(self, user):
        """Returns True if a user has already voted on the exam

        `user`: the user to check whether they had voted

        """
        if ExamVote.select().where((ExamVote.user == user.user_id) & (ExamVote.exam == self.id)).exists():
            return True
        return False

    def has_upvoted(self, user):
        """Returns True if a user has upvoted the exam"""
        if ExamVote.select().where((ExamVote.user == user.user_id) & (ExamVote.exam == self.id) & (ExamVote.upvote == True)).exists():
            return True
        return False

    def vote(self, user, upvote):
        """Allows a user to vote on the exam

        `user`: the User object that is voting
        `upvote`: a boolean representing whether user has upvoted (True) or downvoted (False).

        """
        if not self.has_voted(user):
            try:
                ExamVote.create(
                    user=user.user_id,
                    exam=self.id,
                    upvote=upvote,
                )
            except Exception as e:
                return False, str(e)
        else:
            try:
                ev = ExamVote.get(ExamVote.user == user.user_id, ExamVote.exam == self.id)
                ev.upvote = upvote
                ev.save()
            except Exception as e:
                return False, str(e)
        if upvote:
            self.votes += 1
        else:
            self.votes -= 1
        self.save()
        return True, ""


class ExamVote(Model):
    """Model representing a vote on an exam."""
    id = PrimaryKeyField(db_column='ID')
    user = ForeignKeyField(User, db_column='USER_ID')
    exam = ForeignKeyField(Exam, db_column='EXAM_ID')
    upvote = BooleanField(db_column='UPVOTE')

    class Meta:
        database = DATABASE
        db_table = 'TBL_EXAM_VOTE'
        indexes = (
            (('user', 'exam'), True),
        )
