from playhouse.migrate import migrate, PostgresqlMigrator
from app.models import DATABASE
from app.notes.models import Note

Note.original_filename.default = ''

migrator = PostgresqlMigrator(DATABASE)

migrate(
    migrator.add_column('TBL_NOTE', Note.original_filename.db_column, Note.original_filename)
)

for note in Note.select():
    note.original_filename = note.filename
    note.save()