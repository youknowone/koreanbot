
# -*- coding: utf-8 -*-
from easyirc.client.bot import BotClient

client = BotClient()
client.msgevents = client.events.msgprefix
client.events.msgprefix.prefix = '.'

