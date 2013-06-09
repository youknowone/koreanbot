
# -*- coding: utf-8 -*-
import re
import requests

from bot import client

def daum(word, code=None):
    if code is None:
        nonascii = filter(lambda c: ord(c) > 128, word)
        if len(nonascii) > 0:
            code = 'KUKE'
        else:
            code = 'KUEK'
    response = requests.get('http://dic.daum.net/search.do?q=' + word)
    m = re.search(r'<div class="txt_means_' + code + r'">([^<]*)</div>', response.text)
    if m is None:
        return None
    return m.group(1)


@client.msgevents.hookback('daum', u'다음')
def on_daum(context, message=None):
    """Searches a word from Daum dictionary. Aliases: daum, 다음"""
    if message is None:
        return u'Please suggest keyword'
    result = daum(message)
    if result is None:
        return u'Result not found'
    else:
        return result

