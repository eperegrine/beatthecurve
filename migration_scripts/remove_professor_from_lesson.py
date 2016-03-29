from app.lesson.models import Lesson, Professor
from playhouse.migrate import *
from app.models import DATABASE

for lesson in Lesson.select():
    professors = lesson.professor.split(" & ")
    for professor in professors:
        if professor == 'Unknown':
            Professor.create(lesson_id=lesson.id, first_name='Unknown', last_name='')
        elif professor == 'Instructor: TBA':
            Professor.create(lesson_id=lesson.id, first_name='Instructor: TBA', last_name='')
        else:
            names = professor.split(" ")
            Professor.create(lesson_id=lesson.id, first_name=names[0], last_name=names[1])


migrator = PostgresqlMigrator(DATABASE)

migrate(
    migrator.drop_column('TBL_LESSON', 'PROFESSOR')
)