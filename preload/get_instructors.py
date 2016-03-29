import requests
from lxml import html
import json

x = open("data.json", "r")
d = json.load(x)
print(d)

base_url = "https://ntst.umd.edu"
i = 1
for key in d.keys():
    if d[key]["link"] is not None:
        r = requests.get(base_url + d[key]["link"])
        tree = html.fromstring(r.content)
        for course in tree.cssselect("#" + key):
            professors = set()
            print(i)
            i += 1
            try:
                [professors.add(e.text) for e in course.cssselect(".section-instructor")]
            except:
                continue

            print(professors)
            d[key]["professors"] = list(professors)

print(d)
f = open("data2.json", "w")
json.dump(d, f)