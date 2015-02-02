
# -*- coding: utf-8 -*-
from easyirc.storage import make_storage
from easyirc.const import *
from easyirc import util
from bot import client

visitors = make_storage('visitors.json', lambda key: key)

@client.events.hookmsg(JOIN)
def on_join(connection, sender, chan):
    """Say hello to newface."""
    if chan != '#korean':
        return
    identity = util.parseid(sender)
    users = visitors._get(chan)
    if not users:
        users = []
    name = u'!'.join((identity.nick, identity.username))
    if not name in users:
        if name[:8] == 'ChangeMe':
            connection.privmsg(chan, u'안녕하세요 {nick}님! Welcome to {chan}! You can change your name with "/nick new_name".'.format(chan=chan, nick=identity.nick))
        else:
	    connection.privmsg(chan, u'안녕하세요 {nick}님! Welcome to {chan}!'.format(chan=chan, nick=identity.nick))
            users.append(name)
            visitors._set(chan, users)
            visitors._commit()
