from playhouse.migrate import *
from app.models import DATABASE
from app.exams.models import Exam

migrator = PostgresqlMigrator(DATABASE)

migrate(
    migrator.add_column("TBL_EXAM", Exam.semester.db_column, Exam.semester),
    migrator.add_column("TBL_EXAM", Exam.year.db_column, Exam.year)
)
