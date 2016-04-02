from urllib.request import urlretrieve
import os
from lxml import html
import requests
import redis
from rq import Queue
import subprocess
import sys
import peewee

DATABASE = peewee.SqliteDatabase("preload/exams/exams.db")


class Exam(peewee.Model):
    name = peewee.CharField()
    professor = peewee.CharField(null=True)
    pages = peewee.IntegerField()
    exam_code = peewee.CharField()
    class_code = peewee.CharField()
    term = peewee.CharField()

    class Meta:
        database = DATABASE

DATABASE.create_table(Exam, safe=True)

REDIS_SERVER = redis.Redis("localhost")
REDIS_QUEUE = Queue(connection=REDIS_SERVER)


BASE_URL = 'https://koofers.com'
STUDY_MATERIALS_URL = BASE_URL + '/university-of-maryland-umd/study-materials'
BASE_EXAM_URL = 'https://koofers.com/files/exam-'


def get_image(url):
    server_filename = url.split("/")[-1].split("?")[0]
    code_and_page = server_filename.split("_")
    if len(code_and_page) == 1:
        code_and_page.append("Page_1.jpg")
        code_and_page[0] = code_and_page[0].split(".")[0]
    directory_path = "preload/exams/img/" + code_and_page[0] + "/"
    local_filename = directory_path + "_".join(code_and_page[1:])
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)
    urlretrieve(url, local_filename)


def scrape_page(page_num):
    payload = {'exams': '', 'p': page_num}
    page = requests.get(STUDY_MATERIALS_URL, params=payload)

    tree = html.fromstring(page.content)

    divs = tree.cssselect(".row[onclick]")

    for div in divs:
        REDIS_QUEUE.enqueue(parse_div, html.tostring(div))


def parse_div(div_s):
    # Get name
    div = html.fromstring(div_s)
    title_link = div.cssselect('.title > a')[0]
    name = title_link.text

    # Get link to detail page
    detail_url = title_link.get('href')

    # Get number of pages
    info_spans = div.cssselect(".attr")

    pages = 0
    prof_link = None
    prof_short_name = None

    for span in info_spans:
        info_caption = span.cssselect(".name")[0]

        # Get number of pages
        if info_caption.text == "Pages:":
            pages = span.cssselect(".value")[0].text
            pages = int(pages)

        elif info_caption.text == "Professor:":
            prof_links = span.cssselect(".value a")
            if len(prof_links) > 0:
                prof_short_name = prof_links[0].text
                prof_link = prof_links[0].get('href')

    # Get professor's full name
    prof_name = None

    if prof_short_name in REDIS_SERVER.hgetall("professors").keys():
        prof_name = REDIS_SERVER.hgetall("professors")[prof_short_name]

    elif prof_link is not None:
        prof_page = requests.get(BASE_URL + prof_link)
        prof_tree = html.fromstring(prof_page.content)
        prof_name = prof_tree.cssselect('#full_name')[0].text
        profs = REDIS_SERVER.hgetall("professors")
        profs[prof_short_name] = prof_name
        REDIS_SERVER.hmset('professors', profs)

    # Visit detail page
    detail_page = requests.get(BASE_URL + detail_url)
    detail_tree = html.fromstring(detail_page.content)
    detail_table_rows = detail_tree.cssselect("tr")

    class_code = None
    term = None

    for row in detail_table_rows:
        # Get class code
        cells = row.cssselect("td")
        if cells[0].text == "Class:":
            class_code = cells[1].cssselect("a")[0].text.split("-")[0].replace(" ", "")

        # Get term
        elif cells[0].text == "Term:":
            term = cells[1].text

    # Get preview image div
    preview_images_div = detail_tree.cssselect("#koofer_preview_images")[0]
    first_image = preview_images_div.cssselect("img")[0]
    image_url = first_image.get("src")
    filename = image_url.split("/")[-1]
    exam_code = filename.split("_")[0]

    DATABASE.connect()
    Exam.create(
        name=name,
        professor=prof_name,
        pages=pages,
        exam_code=exam_code,
        class_code=class_code,
        term=term
    )
    DATABASE.commit()
    DATABASE.close()
    REDIS_QUEUE.enqueue(download_exam_images, BASE_EXAM_URL+exam_code, pages)


def download_exam_images(url, pages):
    cmd = ["preload/exams/phantomjs", "preload/exams/download_images.js", url, str(pages)]
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE)

    for line in iter(p.stdout.readline, ''):
        print(line)
        s_line = line.decode("utf-8")
        if s_line[:4] == "url:":
            REDIS_QUEUE.enqueue(get_image, s_line[5:])
        elif "done" in s_line:
            print('terminating')
            p.kill()
            break
        sys.stdout.flush()
        pass
    #p.wait()
