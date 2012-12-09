from __future__ import print_function
import requests
import json
import time

CSRF_TOKEN = ''
SESSION_ID = ''
SLEEP_SECONDS = 20
LOGFILE = 'actions.log'
STATEFILE = 'actions.state'

class UnexpectedResultException(Exception):
    pass

class IngressActionMonitor():
    def __init__(self):
        self.minTimestampMs = -1
        
    def write_state(self):
        f=open(STATEFILE, 'w+')
        try:
            f.write(str(self.minTimestampMs))
        finally:
            f.close()
    
    def load_state(self):
        f=open(STATEFILE, 'r+')
        try:
            text = f.read()
            if text:
                self.minTimestampMs = int(text)
                print('Starting at time: ', text)
        finally:
            f.close()

    def getChat(self, minTimestampMs):
        url='http://www.ingress.com/rpcservice'
        
        cookies = dict(csrftoken=CSRF_TOKEN,
                         ACSID=SESSION_ID,
                          __utma="24037858.1398792667.1353108390.1354674320.1354685176.31; __utmb=24037858.24.9.1354685210580",
                          __utmc="24037858",
                          __utmz="24037858.1353108390.1.1.utmcsr=support.google.com|utmccn=(referral)|utmcmd=referral|utmcct=/ingress/answer/2871444",
                        )
        headers = {"X-Requested-With": "XMLHttpRequest",
                   "X-CSRFToken": CSRF_TOKEN,
                   "Referer": r"http://ingress.com/intel",
                   "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.95 Safari/537.11"}
        data = {"desiredNumItems":50,"minLatE6":44769720,"minLngE6":-93665038,"maxLatE6":45136110,"maxLngE6":-92420150,"minTimestampMs":minTimestampMs,"maxTimestampMs":-1,"method":"dashboard.getPaginatedPlextsV2"}
        
        r = requests.post(url, data=json.dumps(data), headers=headers, cookies=cookies)
        return r.text
    
    def messagegen(self):
        jsonStr = self.getChat(self.minTimestampMs)
        responseItems = json.loads(jsonStr)
        
        if 'result' not in responseItems:
            if 'error' in responseItems:
                print(responseItems)
            else:
                raise UnexpectedResultException(jsonStr)
        else:
            responseItemsOrderedAsc = responseItems['result']
            responseItemsOrderedAsc.reverse()
            for message in responseItemsOrderedAsc:
                yield message
                self.minTimestampMs = message[1] + 1
    
    def actiongen(self):
        messages = self.messagegen()
        return (message for message in messages if message[2]['plext']['plextType'] == 'SYSTEM_BROADCAST')

    def monitor(self):
        self.load_state()
        while True:
            for action in self.actiongen():
                yield action
            self.write_state()
            time.sleep(SLEEP_SECONDS)

def log_lines():
    f = open(LOGFILE, 'r')
    try:
        f.seek(0,2)
        while True:
            line = f.readline()
            yield line #None if no new line
    finally:
        f.close()
        
if __name__ == '__main__':
    monitor = IngressActionMonitor()
    f = open(LOGFILE, 'a', 0)
    try:
        for action in monitor.monitor():
            jsonStr = json.dumps(action)
            print(jsonStr, file=f)
    finally:
        f.close()
        
    