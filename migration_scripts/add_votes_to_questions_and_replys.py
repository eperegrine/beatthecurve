from playhouse.migrate import migrate, PostgresqlMigrator
from app.models import DATABASE
from app.qa.models import Question, Reply
migrator = PostgresqlMigrator(DATABASE)

migrate(
    migrator.add_column('TBL_QUESTION', Question.votes.db_column, Question.votes),
    migrator.add_column('TBL_REPLY', Reply.votes.db_column, Reply.votes),
)
