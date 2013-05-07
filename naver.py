
import urllib
import bs4

from bot import client

def naver(word):
    word.replace(u' ', u'%20')
    url = u'http://dic.naver.com/search.nhn?query={word}'.format(word=word).encode('utf-8')
    html = urllib.urlopen(url).read()
    soup = bs4.BeautifulSoup(html)
   
    try:
        return unicode(soup.find_all("dd")[1].get_text()).strip()
    except IndexError:
        return None


@client.msgevents.hook('dic')
@client.msgevents.hook('naver')
def on_naver(connection, manager, sender, msgtype, target, prefix, message=None):
    if message is None:
        connection.sendl(msgtype, target, 'Please suggest keyword')
    else:
        result = naver(message)
        if result is None:
            connection.sendl(msgtype, target, 'Result not found')
        else:
            connection.sendl(msgtype, target, result)

