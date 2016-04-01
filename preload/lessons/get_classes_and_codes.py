from lxml import html
import requests
import json

base_url = 'https://ntst.umd.edu/soc/'

page = requests.get(base_url)


tree = html.fromstring(page.content)

links = tree.cssselect(".course-prefix > a")

data = {}

for link in [a.get('href') for a in links]:
    # make request
    r = requests.get(base_url + link)

    # get all course divs
    r_tree = html.fromstring(r.content)
    courses = r_tree.cssselect(".course")

    for course in courses:
        professors = set()
        course_id = course.cssselect(".course-id")[0].text.replace('"', "'")
        course_title = course.cssselect(".course-title")[0].text

        try:
            course_link = course.cssselect(".toggle-sections-link")[0].get('href')
        except:
            course_link = None

        data[course_id] = {"title": course_title, "link": course_link}
        print({"title": course_title, "link": course_link})
    

f = open('data.json', 'w')
json.dump(data, f)