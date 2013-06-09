
from bot import client

@client.msgevents.hookback('source')
def on_source(context, message=None):
    """Shows the repository of me."""
    return 'https://github.com/youknowone/koreanbot'
