# import json
# from urllib.request import urlretrieve
# import os
# from PIL import Image
# from io import StringIO
# import requests
# import sys
#
# images_urls = sys.argv[1:]
# print(images_urls)


# f = open("exams.json", "r")
# data = json.load(f)
#
# static_file_url = 'https://koofer-files.s3.amazonaws.com/converted/{}_Page_{}.jpg?AWSAccessKeyId=AKIAIDAIYWJ3CDLPX3XA&Expires=1459425437&Signature=0CujeAxmQKHQjUcFoMnC6AF7ymo%3D'
#
# for exam in data['exams']:
#     exam_code = exam['exam-code']
#     total_pages = exam['pages']
#     current_page = 1
#     while current_page <= total_pages:
#         current_page_str = str(current_page) if current_page > 9 else '0' + str(current_page)
#         if not os.path.exists('img/{}'.format(exam_code)):
#             os.makedirs('img/{}'.format(exam_code))
#         r = requests.get(static_file_url.format(exam_code, current_page_str))
#         i = Image.open(StringIO(r.content))
#         i.save("img/{}/Page_{}.jpg".format(exam_code, current_page))
#         #urlretrieve( )
#         current_page += 1


# import requests
# from lxml import html
#
# cookie = {
#     'AWSELB': '57739FA112D946239A2969DD58550557F507F5176E022D5E8AB41AEAF990158FCD5CF5D53FD2E934F8F804EC41CDA5AD24EF1F36AFADBD8E5265F21C3BD386C378927A8445',
#     'PHPSESSID': '6sn9u5iq7o0q6earp7qgtvg4u4',
#     'UserEmail': 'charlie.thomas%40attwoodthomas.net',
# }
#
# r = requests.get('https://koofers.com/files/exam-bqv1gdngw8/', cookies=cookie)
# tree = html.fromstring(r.content)
#
# divs = tree.cssselect('img')
#
# for div in divs:
#     imgs = div.cssselect("img")[0].get('src')
#     print(img_url)
#

from urllib.request import urlretrieve

def get_image(url):
    filename = url.split("/")[-1].split("?")[0]
    urlretrieve(url, filename)