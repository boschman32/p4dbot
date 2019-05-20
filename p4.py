from enum import Enum
import subprocess
import os
import re

class Change:
    user = "Perforce User"
    changelist = ""
    text = ""
    header = ""
    workspace = "WORKSPACE"
    review = ""

class Status(Enum):
    INVALID = 0
    SUBMITTED = 1
    PENDING = 2
    SHELVED = 3

class Perforce:
    server = None
    depot = None
    status = Status.SUBMITTED
    limit = 1
    swarm = ""

class Server:
    host = None
    user = None
    password = None
    decode = 'ISO-8859-1'

class Storage:
    changes = []

class SwarmUrls:
    changelist = ""
    review = ""
    user = ""


def make_status(input):
    if input == "submitted":
        return Status.SUBMITTED
    elif input == "pending":
        return Status.PENDING
    elif input == "selved":
        return Status.SHELVED
    else:
        return Status.INVALID

def init(config):
    perforce = Perforce()
    perforce.server = Server()
    perforce.server.host = config['p4']["host"]
    perforce.server.user = config['p4']["user"]
    perforce.server.password = config['p4']["password"]
    perforce.server.decode = config['p4']["decode"]
    perforce.limit = config['p4']["limit"]
    perforce.status = make_status(config['p4']["status"])
    perforce.depot = config['p4']["depot"]
    perforce.swarm = config['p4']["swarm"]
    return perforce

def check_for_changes(storage,changes):
    new_changes = []
    for change in changes:
        if validate_change(storage.changes,change):
            storage.changes.append(change)
            new_changes.append(change)
    return new_changes


def validate_change(changes,new_change):
    for change in changes:
        if change.changelist == new_change.changelist:
            return False
    return True

def make_swarm_urls(change,perforce):
    swarm_urls = SwarmUrls()
    swarm_urls.user = perforce.swarm + 'users/'+change.user
    swarm_urls.changelist = perforce.swarm + "changes/"+change.changelist
    swarm_urls.review = perforce.swarm+ "reviews/"+change.review
    return swarm_urls
    
def build_command(perforce):
    status = "submitted"
    if perforce.status == Status.PENDING:
        status = "pending"
    elif perforce.status == Status.SHELVED:
        status = "shelved"
    user = ''
    if perforce.server.user != None:
        user = "-u "+ perforce.server.user
    password = ''
    if perforce.server.password != None:
        password = "-P "+perforce.server.password
    depo = ''
    if perforce.depot != None:
        depo = perforce.depot
    host = ""
    if perforce.server.host != None and perforce.server.host != "":
        host = "-p "+perforce.server.host
    
    command = "p4 "+host+" "+user+" "+password+" changes -l -m "+str(perforce.limit)+" -s "+status+" "+depo
    return command

def request_review(perforce):
    return

def request_changes(perforce):
    command = build_command(perforce)
    p4_changes = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True).stdout.readlines()
    regex = r"(Change\s([0-9]+))"
    user_regex = r"\s([\w]+)@([\w-]+)"
    changes = []
    change = Change()
    for line in p4_changes:
        content = line.decode(perforce.server.decode)
        match = re.search(regex,content)
        if match != None:
            user_match = re.search(user_regex,content)
            changelist = match.group(2)
            change = Change()
            changes.append(change)
            change.changelist = changelist
            change.header = content
            change.text = ""
            change.user = user_match.group(1)
            change.workspace = user_match.group(2)
        else:
            change.text += content
        
    return changes
