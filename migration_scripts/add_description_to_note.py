from playhouse.migrate import migrate, PostgresqlMigrator
from app.models import DATABASE
from app.notes.models import Note

Note.description.default = ''

migrator = PostgresqlMigrator(DATABASE)

migrate(
    migrator.add_column('TBL_NOTE', Note.description.db_column, Note.description)
)

