import json
from app.auth.models import School
from app.lesson.models import Lesson

f = open("data2.json")
data = json.load(f)

school = School.get()



for key, value in data.items():
    if value["link"] is not None and "professors" in value.keys() and key != "UNIV100":
        try:
            professors = " & ".join(value["professors"])


        except TypeError:
            professors = "Unknown"


        Lesson.create(
            code=key,
            lesson_name=value["title"],
            professor=professors,
            school_id=school.school_id
        )


