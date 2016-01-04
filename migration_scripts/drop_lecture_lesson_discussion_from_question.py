from playhouse.migrate import *
from app.models import DATABASE
from app.qa.models import Question
migrator = PostgresqlMigrator(DATABASE)

migrate(
    migrator.drop_column('TBL_QUESTION', 'LECTURE'),
    migrator.drop_column('TBL_QUESTION', 'DISCUSSION')
)
