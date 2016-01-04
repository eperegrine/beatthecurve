from playhouse.migrate import *
from app.models import DATABASE
from app.qa.models import Question

Question.lesson.default = 3

migrator = PostgresqlMigrator(DATABASE)

migrate(
    migrator.add_column('TBL_QUESTION', Question.lesson.db_column, Question.lesson)
)