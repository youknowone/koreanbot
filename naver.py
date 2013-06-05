
import requests
import bs4

from bot import client

class lru(object):
    def __init__(self, limit=100):
        self.limit = limit
        self.order = []
        self.cache = {}
    
    def add(self, key, value):
        # Already in cache, reset time
        if key in self.cache:
            self.order.remove(key)
        # New element, but full
        if len(self.order) >= self.limit:
            element = self.order.pop(0)
            del self.cache[element]
        # New element or refreshing content
        self.cache[key] = value
        self.order.append(key)

    def remove(self, key):
        if key in self.cache:
            del self.cache[key]
            self.order.remove(key)

    def get(self, key):
        if key not in self.cache:
            return None
        self.order.remove(key)
        self.order.append(key)
        return self.cache[key]

def naver(word):
    word.replace(u' ', u'%20')
    url = u'http://dic.naver.com/search.nhn?query={word}'.format(word=word).encode('utf-8')
    r = requests.get(url)
    if r.status_code != requests.codes.ok:
        return None
    soup = bs4.BeautifulSoup(r.text)
   
    try:
        text = unicode(soup.find_all("dd")[1].get_text())
    except IndexError:
        return None
    lines = text.replace('\r', '\n').split('\n')
    lines = [line.strip() for line in lines]
    lines = filter(lambda line: len(line) > 0, lines)
    return u' '.join(lines)

LRU_CACHE = lru(256)

@client.msgevents.hook('dic')
@client.msgevents.hookback('naver')
def on_naver(message=None):
    if message is None:
        return u'Please suggest keyword'

    result = LRU_CACHE.get(message)
    if result is not None:
        return result

    result = naver(message)
    if result is None:
        return u'Result not found'
    else:
        LRU_CACHE.add(message, result)
        return result

