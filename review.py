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
    
    def get_handler(self,query):
            if len(query) > 0:
                print '[p4dbot review] recived request ' + str(query)
                review = query.review
                status = query.status
                change = query.change
                project_name = query.projectName
                review_data = p4.request_review(self.perforce)
                

            pass

    def init(self):
        self.server = net.make_server(self.config["server"]["host"],self.config["server"]["port"],self)

    def shutdown(self):
        self.server.socket.close()
    

bot = p4bot_review()
bot.init()
try:
    print '[p4dbot review] start the server'
    bot.server.serve_forever()
except KeyboardInterrupt:
	print '[p4dbot review] shutting down the server'
	bot.shutdown()


