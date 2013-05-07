
import urllib
import bs4

from bot import client

def naver(word):
    word.replace(u' ', u'%20')
    url = u'http://dic.naver.com/search.nhn?query={word}'.format(word=word).encode('utf-8')
    html = urllib.urlopen(url).read()
    soup = bs4.BeautifulSoup(html)
   
    try:
        text = unicode(soup.find_all("dd")[1].get_text())
    except IndexError:
        return None
    lines = text.replace('\r', '\n').split('\n')
    lines = [line.strip() for line in lines]
    lines = filter(lambda line: len(line) > 0, lines)
    return u' '.join(lines)


@client.msgevents.hook('dic')
@client.msgevents.hookback('naver')
def on_naver(message=None):
    if message is None:
        return u'Please suggest keyword'
    result = naver(message)
    if result is None:
        return u'Result not found'
    else:
        return result

