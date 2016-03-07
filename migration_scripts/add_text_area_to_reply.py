from playhouse.migrate import migrate, PostgresqlMigrator
from app.models import DATABASE
from app.qa.models import Reply
migrator = PostgresqlMigrator(DATABASE)

Reply.content.default = ''

migrate(
    migrator.drop_column('TBL_REPLY', Reply.content.db_column),
    migrator.add_column('TBL_REPLY', Reply.content.db_column, Reply.content)
)
