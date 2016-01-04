from playhouse.migrate import *
from app.models import DATABASE
from app.qa.models import Question

Question.document.default = ''

migrator = PostgresqlMigrator(DATABASE)

migrate(
    migrator.add_column('TBL_QUESTION', Question.document.db_column, Question.document)
)