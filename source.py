
from bot import client

@client.msgevents.hookback('source')
def on_source(message=None):
    return 'https://github.com/youknowone/koreanbot'
