import p4
import discord
import utils
import net



class p4bot_review:

    def __init__(self):
        self.storage = p4.Storage()
        try:
            self.config = utils.create_config("config.json")
            self.discord = discord.Discord(self.config)
            self.perforce = p4.init(self.config)
        except AssertionError as error:
                assert False, error

    def run(self):
        self.server = net.make_server(self.config["server"]["host"],self.config["server"]["port"])


bot = p4bot_review()
bot.run()
bot.server.serve_forever()


