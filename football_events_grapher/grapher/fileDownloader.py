import requests
from os import getcwd


def download(url):
    directory = getcwd()
    filename = directory + "\\" + url.rsplit('/', 1)[-1]
    r = requests.get(url)
    f = open(filename, 'w', encoding='utf-8')
    f.write(r.text,)
