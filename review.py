import p4
import discord
import utils
import net


class p4bot_review:

    def __init__(self):
        self.storage = p4.Storage()
        self.reviews = []
        try:
            self.config = utils.create_config("config.json")
            self.discord = discord.Discord(self.config)
            self.perforce = p4.init(self.config)
        except AssertionError as error:
            assert False, error

    def get_handler(self, query):
        if len(query) > 0:
            print '[p4dbot review] recived request ' + str(query)
            review = query['review']
            status = query["status"]
            change = query["change"]
            project_name = query["project_name"]
            review_data = p4.request_review(self.perforce, review)
            if status != 'submitted':
                return self.process(review_data)
            else:
                self.send_notif(review_data)
                self.remove(review_data)
            return "{}"
        pass

    def process(self, review_data):
        if review_data == None:
            return '{error:"No review"}'
        else:
            if self.check_review(review_data):
                return '{result:100}'
            elif self.check_comments(review_data["comments"]):
                return '{result:101}'
            else:
                return '{result:404}'

            return '{result:200}'

    def remove(self, review_data):
        for r in self.reviews:
            if r['data']['id'] == review_data['data']['id']:
                self.reviews.remove(review_data)
                return

    def check_comments(self, comments):
        for comment in self.reviews:
            if len(comment['comments']) != len(comments):
                comment['comments'] = comments
                return True
            else:
                return False

    def check_review(self, review):
        for r in self.reviews:
            if r['data']['id'] == review['data']['id']:
                if r['data']['state'] != review['data']['state']:
                    r = review
                    return True
                elif review['data']['state'] == "archived":
                    self.reviews.remove(r)
                    return False
                else:
                    return False
        if review['data']['state'] != "archived":
            self.reviews.append(review)
            return True
        else:
            return False

    def send_notif(self, review):
        return

    def init(self):
        self.server = net.make_server(
            self.config["server"]["host"], self.config["server"]["port"], self)

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
