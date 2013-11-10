from urllib.request import urlopen
import shelve

cache = shelve.open("cache")

def clear_cache():
    for url in cache:
        del cache[url]

def uncache(url):
    if url in cache:
        del cache[url]

def download(url):
    if url in cache:
        return cache[url]
    html = urlopen(url).read().decode('utf-8')
    return html

