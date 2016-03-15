from playhouse.migrate import PostgresqlMigrator, migrate
from app.models import DATABASE
from app.qa.models import Question

migrator = PostgresqlMigrator(DATABASE)

Question.content.default = ''

contents = {}

for question in Question.select():
    contents[question.id] = question.content

print(contents)

migrate(
    migrator.drop_column('TBL_QUESTION', 'CONTENT'),
    migrator.add_column('TBL_QUESTION', Question.content.db_column, Question.content)
)

for question in Question.select():
    question.content = contents[question.id]
    question.save()

