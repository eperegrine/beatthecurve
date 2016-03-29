import json
from app.auth.models import School
from app.lesson.models import Lesson, Professor

f = open("data2.json")
data = json.load(f)

school = School.get()

for key, value in data.items():
    if value["link"] is not None and "professors" in value.keys() and key != "UNIV100":
        lesson = Lesson.create(
            code=key,
            lesson_name=value["title"],
            school_id=school.school_id
        )

        if value["professors"][0] is not None:
            for p in value["professors"]:
                name = p.split(" ")
                Professor.create(
                    lesson=lesson.id,
                    first_name=name[0],
                    last_name=name[1]
                )


