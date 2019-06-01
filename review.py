import p4
import discord
import utils
import net
import time
import re
from threading import Thread, Lock
mutex = Lock()


class p4bot_review:

    def __init__(self):
        self.storage = p4.Storage()
        self.reviews = {}
        self.exit_flag = True
        try:
            self.config = utils.create_config("config.json")
            self.discord = discord.Discord(self.config, "review_webhook")
            self.perforce = p4.init(self.config)
        except AssertionError as error:
            mutex.acquire()
            self.exit_flag = False
            mutex.release()
            assert False, error

    def get_handler(self, query):
        if len(query) > 0:
            print '[p4dbot review] recived request ' + str(query)
            review = query['review']
            status = query["status"]
            change = query["change"]
            project_name = query["project_name"]
            review_data = p4.request_review(self.perforce, review[0])
            mutex.acquire()
            if review_data['data']['state'] != "archived":
                self.need_to_add(review[0], review_data)
            mutex.release()
            return "{}"
        pass

    def need_to_add(self, rId, review):
        reviewObject = self.reviews.get(rId)
        if reviewObject == None:
            self.reviews.update({rId: review})
            self.notif(review)
        else:
            self.validate(reviewObject, review)

    def validate(self, reviewA, reviewB):
        if reviewA['data']['state'] != reviewB['data']['state']:
            self.status_changed(reviewB)
            return True
        elif len(reviewA['comments']) != len(reviewB['comments']):
            self.comments_changed(reviewB)
            return True
        return False

    def comments_changed(self, review):
        self.reviews.update({review['id']: review})
        self.notif(review,True)

    def status_changed(self, review):
        self.reviews.update({review['id']: review})
        self.notif(review)

    def clear(self):
        return

    def process(self):
        while self.exit_flag:
            for (key, review) in self.reviews.items():
                mutex.acquire()
                review_data = p4.request_review(self.perforce, key)
                if review_data != None:
                    state = review_data["data"]["state"]
                    self.need_to_add(key, review_data)
                    if state == "archived":
                        del self.reviews[key]

                mutex.release()
            time.sleep(self.config["pull_interval"])

    def find_user(self,user):
        for users in self.config['discord']['users']:
            if users['swarm'] == user:
                return users["discord"]
        return user

    def mention(self,text,user):
        regex = r"(@"+user+")"
        subst = "<@"+self.find_user(user)+">"
        # You can manually specify the number of replacements by changing the 4th argument
        return re.sub(regex, subst, text, 0, re.MULTILINE)

    def mentions(self,text):
        for users in self.config['discord']['users']:
            regex = r"(@"+users['swarm']+")"
            subst = "<@"+users['discord']+">"
            # You can manually specify the number of replacements by changing the 4th argument
            text = re.sub(regex, subst, text, 0, re.MULTILINE)
        return text

    def notif(self, review,comment = False):
        review = review['data']
        change = p4.Change()
        change.user = review['author']
        change.changelist = str(review['changes'][len(review['changes'])-1])
        change.review = str(review['id'])
        swarm_urls = p4.make_swarm_urls(change, self.perforce)
        message = discord.Message()
        message.user = change.user

        if review['state'] != 'approved':
            message.color = 0x7CFC00
        elif review['state'] != 'archived':
            message.color = 0xFFA500
        else:
            message.color = 0xc8702a

        if not comment:
            message.header = "Review #"+str(review['id'])+" Request from " + \
                change.user+" Status: "+review['stateLabel']
        else:
            message.header = "Review #"+str(review['id'])+" Request from " + \
                change.user+" New Comment!"
        
        message.content = self.mentions(review['description'])+' Author:'+self.mentions("@"+review['author'])
        message.footer = swarm_urls.review
        message.url =  swarm_urls.review
        self.discord.send(message)
        return

    def init(self):
        self.server = net.make_server(
            self.config["server"]["host"], self.config["server"]["port"], self)
        self.processThread = Thread(target=self.process)
        self.processThread.start()

    def shutdown(self):
        self.server.socket.close()
        mutex.acquire()
        try:
            self.exit_flag = False
        finally:
            mutex.release()
        self.processThread.join()


bot = p4bot_review()
bot.init()
try:
    print '[p4dbot review] start the server'
    bot.server.serve_forever()
except KeyboardInterrupt:
    print '[p4dbot review] shutting down the server'
    bot.shutdown()
