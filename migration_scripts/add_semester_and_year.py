from playhouse.migrate import *
from app.models import DATABASE
from app.notes.models import Lecture

migrator = PostgresqlMigrator(DATABASE)

migrate(
    migrator.add_column("TBL_LECTURE", Lecture.semester.db_column, Lecture.semester),
    migrator.add_column("TBL_LECTURE", Lecture.year.db_column, Lecture.year)
)
