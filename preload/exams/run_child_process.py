import subprocess
import sys
from urllib.request import urlretrieve
from redis import Redis
from rq import Queue
from download_images import get_image

q = Queue(connection=Redis())



cmd = ["./phantomjs", "download_images.js"]
p = subprocess.Popen(cmd, stdout=subprocess.PIPE)

urls = []

for line in iter(p.stdout.readline, ''):
    print(line)
    if line.decode("utf-8")[:4] == "url:":
        print(line.decode('utf-8')[5:])
        q.enqueue(get_image, line.decode('utf-8')[5:])

    sys.stdout.flush()
    pass
p.wait()

print(urls)