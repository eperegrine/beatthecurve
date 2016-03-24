from playhouse.migrate import migrate, PostgresqlMigrator
from app.models import DATABASE
from app.notes.models import Note


migrator = PostgresqlMigrator(DATABASE)

migrate(
    migrator.add_column('TBL_NOTE', Note.datetime.db_column, Note.datetime)
)

