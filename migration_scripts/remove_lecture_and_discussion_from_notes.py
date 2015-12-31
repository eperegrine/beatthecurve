from playhouse.migrate import *
from app.models import DATABASE
from app.notes.models import Note

migrator = PostgresqlMigrator(DATABASE)

migrate(
    migrator.drop_column('TBL_NOTE', 'DISCUSSION'),
    migrator.drop_column('TBL_NOTE', 'LECTURE')
)
