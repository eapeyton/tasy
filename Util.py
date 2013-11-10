from urllib.request import urlopen
import shelve

class Downloader:
    def __enter__(self):
        self.cache = shelve.open("cache")
        return self

    def clear_cache(self):
        for url in self.cache:
            del self.cache[url]

    def uncache(self, url):
        if url in self.cache:
            del self.cache[url]

    def download(self, url):
        if url in self.cache:
            return self.cache[url]
        else:
            html = urlopen(url).read().decode('utf-8')
            self.cache[url] = html
            return html

    def __exit__(self, type, value, traceback):
        self.cache.close()


