from playhouse.migrate import migrate, PostgresqlMigrator
from app.models import DATABASE
from app.lesson.models import LessonStudent

migrator = PostgresqlMigrator(DATABASE)

LessonStudent.semester.default = 1
LessonStudent.year.default = 2015

migrate(
    migrator.add_column('TBL_LESSON_STUDENT', LessonStudent.semester.db_column, LessonStudent.semester),
    migrator.add_column('TBL_LESSON_STUDENT', LessonStudent.year.db_column, LessonStudent.year),
)
