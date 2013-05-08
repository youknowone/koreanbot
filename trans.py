
import json
import requests

from bot import client

def trans(line, sl, tl, mode=2):
    url = 'http://translator.suminb.com/v1.0/translate'
    response = requests.post(url, dict(sl=sl, tl=tl, m=mode, t=line.encode('utf-8')))
    data = json.loads(response.text)
    return data['translated_text']

def on_tr(message=None, mode=2):
    if message is None:
        return u'Please suggest sentence to translate'
    parts = message.split(' ', 1)
    if parts[0] == 'en':
        sl = 'en'
        tl = 'ko'
        ln = parts[1]
    elif parts[0] == 'ko':
        sl = 'ko'
        tl = 'en'
        ln = parts[1]
    else:
        ln = message
        testln = filter(lambda c: ord(c) >= 128, ln)
        if len(testln) == 0:
            sl = 'en'
            tl = 'ko'
        else:
            sl = 'ko'
            tl = 'en'
    
    result = trans(ln, sl, tl, mode)
    if result is None:
        return u'Result not found'
    else:
        return result

@client.msgevents.hookback('tr1')
def on_tr1(message=None):
    return on_tr(message, 1)

@client.msgevents.hookback('tr')
def on_tr2(message=None):
    return on_tr(message, 2)

