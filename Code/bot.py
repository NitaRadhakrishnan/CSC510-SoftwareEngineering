import time
import event
from slackclient import SlackClient

 
class Bot(object):
    def __init__(self):
        self.slack_client = SlackClient("xoxb-795814705207-788531806065-9dWeyIRqj2t1LSbICYnDkB01")
        self.botname = "libbot"
        self.bot_id = self.getbotid()
         
        if self.bot_id is None:
            exit("Error, could not find " + self.botname)
     
        self.event = event.Event(self)
        self.listen()
     
    def getbotid(self):
        api_call = self.slack_client.api_call("users.list")
        if api_call.get('ok'):
            users = api_call.get('members')
            for user in users:
                if 'name' in user and user.get('name') == self.botname:
                    return "<@" + user.get('id') + ">"
            return None
             
    def listen(self):
        if self.slack_client.rtm_connect(with_team_state=False):
            print ("Successfully connected, listening for commands")
            while True:
                self.event.waitforevent()
                 
                time.sleep(1)
        else:
            exit("Error, Connection Failed")