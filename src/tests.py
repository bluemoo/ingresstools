import random
import datetime
import unittest

class IngressPlayer():
    def __init__(self, playerNode):
        self.playerNode = playerNode
        self.name = playerNode[1]['plain']
        
class ActionBroadcast():
    def __init__(self, messageNode):
        self.messageNode = messageNode
        self.plext = self.messageNode[2]['plext']
        self.player = IngressPlayer(self.plext['markup'][0])
    def when(self):
        ts_in_ms = self.messageNode[1]
        ts = ts_in_ms/1000
        return datetime.datetime.fromtimestamp(ts)
    
    def is_resistance(self):
        return self.plext['team'] == 'RESISTANCE'
    
    
class ActionBroadcastTest(unittest.TestCase):

    def test_should_parse_correctly(self):
        action = ActionBroadcast(["2f6cc9c0b3f1440ebf32d1d1f4892ba9.d", 1354859490381, {"plext": {"text": "fluffysquid deployed an L1 Resonator on Robert Trail Library (Rosemount, MN, United States)", "markup": [["PLAYER", {"plain": "fluffysquid", "guid": "4f183b0793b84f3e83e9d7e6cddbc664.c", "team": "RESISTANCE"}], ["TEXT", {"plain": " deployed an "}], ["TEXT", {"plain": "L1"}], ["TEXT", {"plain": " Resonator on "}], ["PORTAL", {"name": "Robert Trail Library", "plain": "Robert Trail Library (Rosemount, MN, United States)", "team": "RESISTANCE", "latE6": 44740652, "address": "Rosemount, MN, United States", "lngE6": -93126793, "guid": "f274aa45432e48dfbd2baea99924285d.12"}]], "plextType": "SYSTEM_BROADCAST", "team": "RESISTANCE"}}])
        self.assertEqual(datetime.datetime(2012, 12, 6, 23, 51, 30), action.when() )
        self.assertEqual(True, action.is_resistance())
        self.assertEqual('fluffysquid', action.player.name)
        
if __name__ == '__main__':
    unittest.main()