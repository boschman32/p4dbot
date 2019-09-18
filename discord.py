from discord_webhook import DiscordWebhook, DiscordEmbed

class discord_data:
    url = None
    name = None

class Message:
    header = ""
    content = ""
    user = ""
    footer = ""
    color = 0xc8702a

class Discord:
    def __init__(self,config):
        self.data = discord_data()
        self.data.url = config['discord']['webhook_url']
        self.data.name = config['discord']['name']
        self.webhook = DiscordWebhook(self.data.url)
       

    def send(self,message):
        if self.webhook != None:
            embed = DiscordEmbed(title='%s' % (message.header), description='%s' % (message.content), color=message.color)
            embed.set_author(name=message.user)
            embed.set_footer(text=message.footer, ts=True)

            self.webhook.add_embed(embed)
            self.webhook.execute()
        else:
            assert False,"Discord was not initilized"