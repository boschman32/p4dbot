import time
import p4
import discord
import utils

class p4bot_commit:

    def __init__(self):
        self.storage = p4.Storage()
        try:
            self.config = utils.create_config("config.json")
            self.discord = discord.Discord(self.config, "commit_webhook")
            self.perforce = p4.init(self.config)
        except AssertionError as error:
                assert False, error

    def make_content(self, change):
        content = change.header + change.text
        return content

    def send_changes(self, _changes):
        messages = []
        changes = self.filter(_changes)
        print "[p4bot] sends "+str(len(changes))+" messages"
        for change in changes:
            swarm_urls = p4.make_swarm_urls(change, self.perforce)
            message = discord.Message()
            message.user = change.user
            message.header = change.header.replace(
                change.changelist, swarm_urls.changelist)
            message.content = change.text
            messages.append(message)
            message.footer = swarm_urls.changelist
            message.color = self.get_color(change)
            self.discord.send(message)

    def filter(self, changes):
        if self.config['use_filter']:
            filtered_changes = []
            for change in changes:
                if self.has_filter(change):
                    filtered_changes.append(change)
            return filtered_changes
        else:
            return changes

    def has_filter(self, change):
        for filter in self.config["filters"]:
            if change.text.lower().find(filter["tag"].lower()) != -1:
                return True
        return False

    def get_color(self, change):
        for filter in self.config["filters"]:
            if change.text.lower().find(filter["tag"].lower()) != -1:
                    return int(filter['color'],16)
        return 0xc8702a

    def pull(self):
        interval = float(self.config["pull_interval"])
        timer = time.time()
        while True:
            try:
                changes = p4.request_changes(self.perforce)
                new_changes = p4.check_for_changes(self.storage,changes)
                print "[p4bot] found "+str(len(new_changes))+" changes"
                self.send_changes(new_changes)
                time.sleep(interval - ((time.time() - timer) % interval))
            except  AssertionError as error:
                assert False,error
            except KeyboardInterrupt:
                print "[p4bot] shutdown"
                quit()

if __name__ == "__main__":
    app = p4bot_commit()
    print "[p4bot_commit] will pull every "+str(app.config['pull_interval'])+" seconds from "+app.config['p4']["host"]
    app.pull()
