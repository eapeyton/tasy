from urllib.request import urlopen
def download(url):
    html = urlopen(url).read()
    return html

