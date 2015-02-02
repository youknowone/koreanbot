
# -*- coding: utf-8 -*-
import requests
import bs4
import threading
import re

from bot import client

import settings

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

def shorten(url, resp):
    r = requests.post('http://v.gd/create.php', {
        'format':'json', 'url':url })
    if r.status_code == requests.codes.ok:
        j = r.json()
        if 'shorturl' in j:
            resp.append("%s" % j['shorturl'])

def parentheses(string):
    parens = re.sub(r'(\d\.)', r'(\1)', string)
    return parens.replace('.', '')

def space(string):
	indicies = [m.start() for m in re.finditer('(\d)', string)]
	chars = list(string)
	i = 0
	for x in indicies:
		if x != 0:
			chars.insert(x + i, ' ')
			i = i + 1
	return u''.join(chars)

def naver(word):
    word.replace(u' ', u'%20')
    url = u'http://dic.naver.com/search.nhn?query={word}'.format(word=word).encode('utf-8')

    # spawn an async fetch
    shorter = []
    t = threading.Thread(target=shorten, args=(url, shorter))
    t.start()

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

    t.join()
    unspaced_definitions = u' '.join(lines)
    definitions = parentheses(space(unspaced_definitions))
    short_link = u''.join(shorter)
    text = definitions + ' ' + short_link
    return text

try:
    CACHE_SIZE = settings.NAVER_CACHE_SIZE
except AttributeError:
    CACHE_SIZE = 256

LRU_CACHE = lru(CACHE_SIZE)

@client.msgevents.hookback(u'얓')
@client.msgevents.hookback('dic', u'사전')
@client.msgevents.hookback('naver', u'네이버')
def on_naver(context, message=None):
    u"""Searches a word from Naver dictionary. Aliases: naver, 네이버, dic, 사전, 얓"""
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

