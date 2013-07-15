
# -*- coding: utf-8 -*-
import requests
import threading
from datetime import datetime
from pytz import timezone

from bot import client

import settings

@client.msgevents.hookback('date', u'일자')
def on_date(context, message=None):
    u"""Prints the date in KR time."""
    if message is None:
        return u'Please suggest keyword'

    now = datetime.now(timezone('Asia/Seoul'))
    if now.hour < 12:
        fmt = u'%a %Y년 %m월 %d일 오전 %I:%M:%S %z %Z'
        return now.strftime(fmt.encode('utf-8')).decode('utf-8')
    else
        fmt = u'%a %Y년 %m월 %d일 오후 %I:%M:%S %z %Z'
        return now.strftime(fmt.encode('utf-8')).decode('utf-8')
