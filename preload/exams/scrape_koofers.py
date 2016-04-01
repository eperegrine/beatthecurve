from lxml import html
import requests
import json

base_url = 'https://koofers.com'
study_materials_url = base_url + '/university-of-maryland-umd/study-materials'

payload = {'exams': '', 'p': 1}

data = {'exams': []}

while payload['p'] < 450:
    page = requests.get(study_materials_url, params=payload)

    tree = html.fromstring(page.content)

    divs = tree.cssselect(".row[onclick]")

    for div in divs:

        # Get name
        title_link = div.cssselect('.title > a')[0]
        name = title_link.text

        # Get link to detail page
        detail_url = title_link.get('href')

        # Get number of pages
        info_spans = div.cssselect(".attr")

        pages = 0
        prof_link = None

        for span in info_spans:
            info_caption = span.cssselect(".name")[0]

            # Get number of pages
            if info_caption.text == "Pages:":
                pages = span.cssselect(".value")[0].text
                pages = int(pages)

            elif info_caption.text == "Professor:":
                prof_links = span.cssselect(".value a")
                if len(prof_links) > 0:
                    prof_link = prof_links[0].get('href')

        # Get professor's full name
        prof_name = None

        if prof_link is not None:
            prof_page = requests.get(base_url + prof_link)
            prof_tree = html.fromstring(prof_page.content)
            prof_name = prof_tree.cssselect('#full_name')[0].text

        # Visit detail page
        detail_page = requests.get(base_url + detail_url)
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

        data['exams'].append({
            'name': name,
            'professor': prof_name,
            'pages': pages,
            'exam-code': exam_code,
            'class-code': class_code,
            'term': term,
        })

    print("Done page: " + str(payload['p']))
    payload['p'] += 1
    f = open("preload/exams/exams.json", "w")
    json.dump(data, f)
