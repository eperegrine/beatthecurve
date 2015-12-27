from playhouse.migrate import *
from app.models import DATABASE
from app.auth.models import UserPermission

migrator = PostgresqlMigrator(DATABASE)

migrate(
    migrator.add_index('TBL_USER_PERMISSION', (UserPermission.user.db_column, UserPermission.permission.db_column), True)
)
