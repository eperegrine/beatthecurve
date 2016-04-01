from urllib.request import urlretrieve
import os

def get_image(url):
    server_filename = url.split("/")[-1].split("?")[0]
    code_and_page = server_filename.split("_")
    directory_path = "preload/exams/img/" + code_and_page[0] + "/"
    local_filename = directory_path + "_".join(code_and_page[1:])
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)
    urlretrieve(url, local_filename)