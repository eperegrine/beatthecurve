from playhouse.migrate import migrate, PostgresqlMigrator
from app.models import DATABASE
from app.exams.models import Exam


migrator = PostgresqlMigrator(DATABASE)

migrate(
    migrator.add_column('TBL_EXAM', Exam.description.db_column, Exam.description)
)

