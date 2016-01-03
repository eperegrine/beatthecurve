from app.models import DATABASE
from app.auth.models import School, User, Permission, UserPermission
from app.lesson.models import Lesson, LessonStudent
from app.notes.models import Lecture, Discussion, Note, NoteVote
from app.qa.models import Question, Reply
from app.exams.models import Exam, ExamVote
from app.studygroups.models import StudyGroup, StudyGroupComment, StudyGroupMembers, StudyGroupSession
from app.search.models import Option, UserOption
from app.chat.models import Message

DATABASE.create_tables([School, User, Permission, UserPermission, Lesson, LessonStudent, Lecture, Discussion, Note,
                        NoteVote, Question, Reply, Exam, ExamVote, StudyGroup, StudyGroupComment, StudyGroupMembers,
                        StudyGroupSession, Option, UserOption, Message], safe=True)