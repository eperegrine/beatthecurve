from playhouse.migrate import *
from app.models import DATABASE
from app.auth.models import Permission

migrator = PostgresqlMigrator(DATABASE)

migrate(
    migrator.add_index('TBL_PERMISSION', (Permission.name.db_column, Permission.school.db_column), True)
)
