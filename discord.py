from discord_webhooks import DiscordWebhooks

class discord_data:
    url = None
    name = None

class Message:
    header = ""
    content = ""
    user = ""
    footer = ""
    color = 0xc8702a
    url = None

class Discord:
    def __init__(self,config,webhook):
        self.data = discord_data()
        self.data.url = config['discord']['webhooks'][webhook]['url']
        self.data.name = config['discord']['webhooks'][webhook]['name']
        self.webhook = DiscordWebhooks(self.data.url)

    def send(self,message):
        if self.webhook != None:
            if message.url != None:
                self.webhook.set_content(color=message.color, title='%s' % (message.header),description='%s' % (message.content),url=message.url)
            else:
                self.webhook.set_content(color=message.color, title='%s' % (message.header),description='%s' % (message.content))
            self.webhook.set_author(name=message.user)
            self.webhook.set_footer(text=message.footer, ts=True)
            self.webhook.send()
        else:
            assert False,"Discord was not initilized"