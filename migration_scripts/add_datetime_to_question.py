from playhouse.migrate import migrate, PostgresqlMigrator
from app.models import DATABASE
from app.qa.models import Question


migrator = PostgresqlMigrator(DATABASE)

migrate(
    migrator.add_column('TBL_QUESTION', Question.datetime.db_column, Question.datetime)
)

