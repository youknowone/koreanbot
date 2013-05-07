
from bot import client

@client.msgevents.hook('source')
def on_source(connection, manager, sender, msgtype, target, prefix, message=None):
    connection.sendl(msgtype, target, 'https://github.com/youknowone/koreanbot')
