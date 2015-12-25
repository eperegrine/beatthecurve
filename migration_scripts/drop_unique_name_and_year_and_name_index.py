from playhouse.migrate import *
from app.models import DATABASE
from app.notes.models import Lecture

migrator = PostgresqlMigrator(DATABASE)

migrate(
    migrator.drop_index('TBL_LECTURE', 'TBL_LECTURE_NAME'),
    migrator.add_index('TBL_LECTURE', (Lecture.name.db_column, Lecture.year.db_column, Lecture.lesson_id.db_column), True)
)
