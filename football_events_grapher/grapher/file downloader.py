import requests
from os import getcwd


def download(url):
    directory = getcwd()
    filename = directory + "\\" + url.rsplit('/', 1)[-1]
    r = requests.get(url)
    f = open(filename, 'w')
    f.write(r.text)


download("https://raw.githubusercontent.com/statsbomb/open-data/master/data/events/15946.json")
