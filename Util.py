from urllib.request import urlopen
def download(url):
    html = urlopen(url).read().decode('utf-8')
    return html

