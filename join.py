
# -*- coding: utf-8 -*-
from easyirc.storage import make_storage
from easyirc.const import *
from easyirc import util
from bot import client

visitors = make_storage('visitors.json', lambda key: key)

@client.events.hookmsg(JOIN)
def on_join(connection, sender, chan):
    identity = util.parseid(sender)
    users = visitors._get(chan)
    if not users:
        users = []
    name = u'!'.join((identity.nick, identity.username))
    if not name in users:
        connection.privmsg(chan, u'안녕하세요 {nick}님! {chan}에 처음 오신 것을 환영해요. Welcome to {chan}!'.format(chan=chan, nick=identity.nick))
        connection.notice('Pikmeir', u'New visitor! XD')
        users.append(name)
        visitors._set(chan, users)
        visitors._commit()
