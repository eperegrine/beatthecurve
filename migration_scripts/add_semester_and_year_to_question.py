from playhouse.migrate import *
from app.models import DATABASE
from app.qa.models import Question

migrator = PostgresqlMigrator(DATABASE)

migrate(
    migrator.add_column("TBL_QUESTION", Question.semester.db_column, Question.semester),
    migrator.add_column("TBL_QUESTION", Question.year.db_column, Question.year)
)
