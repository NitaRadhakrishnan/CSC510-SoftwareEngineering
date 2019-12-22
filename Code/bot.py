""" BOT.PY """
import json
import time
from slackclient import SlackClient
import command
import event


with open("/home/CSC510-23/Code/data.json") as json_file:
    DATA = json.load(json_file)
TOKEN = DATA["SLACK_BOT_TOKEN"]


class Bot(object):
    """ BOT CLASS """
    def __init__(self):
        self.slack_client = SlackClient(TOKEN)
        self.botname = "l.i.b.r.a"
        self.botid = self.getbotid()
        if self.botid is None:
            exit("Error, could not find " + self.botname)
        self.event = event.Event(self)
        self.command = command.Command()
        self.listen()

    def getbotid(self):
        """ Get the bot id """
        api_call = self.slack_client.api_call("users.list")
        if api_call.get('ok'):
            users = api_call.get('members')
            for user in users:
                if 'name' in user and user.get('name') == self.botname:
                    return user.get('id')
        return None

    def listen(self):
        """ Channel Listening """
        if self.slack_client.rtm_connect(with_team_state=False):
            while True:
                self.event.waitforevent()

                time.sleep(1)
        else:
            exit("Error, Connection Failed")
